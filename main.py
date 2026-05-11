# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware import Middleware
from sqlalchemy.orm import Session
from typing import List

import models, database, schemas, tasks
from middleware import log_requests

# --- Application Setup ---

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app with custom middleware
app = FastAPI(title="Enhanced Shop API", middleware=[Middleware(log_requests)])

# --- Dependency ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Routes ---

@app.post("/api/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Admin endpoint to create a new product."""
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/api/products", response_model=List[schemas.ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all available products."""
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

@app.post("/api/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order. This is a simplified version that doesn't handle
    user authentication or stock deduction for brevity.
    """
    total_price = 0
    order_items = []

    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found.")
        
        if product.stock_quantity < item.quantity:
             raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}.")

        item_total = product.price * item.quantity
        total_price += item_total
        
        # In a real app, you'd create OrderItem models here
        order_items.append({"product_name": product.name, "quantity": item.quantity, "subtotal": item_total})
        
        # Deduct stock
        product.stock_quantity -= item.quantity

    # Create the order (simplified, without a real user)
    db_order = models.Order(total_price=total_price, user_id=1) # Placeholder user_id
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Trigger the background email task
    # In a real app, you'd get the user's email from the database
    tasks.send_order_confirmation_email.delay("customer@example.com", db_order.id, db_order.total_price)

    return db_order