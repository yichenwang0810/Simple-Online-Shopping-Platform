# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    description: str
    stock_quantity: int = Field(..., ge=0, description="Stock cannot be negative")

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

# --- Order Schemas ---
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    product_name: str
    quantity: int
    subtotal: float
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    items: List[OrderItemResponse]
    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True