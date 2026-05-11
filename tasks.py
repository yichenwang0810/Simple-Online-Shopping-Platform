# tasks.py
from celery import Celery
import time

# Configure Celery to use Redis as the message broker
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def send_order_confirmation_email(user_email: str, order_id: int, total_price: float):
    """
    A background task to simulate sending an order confirmation email.
    In a real application, you would use an email service like SendGrid or AWS SES.
    """
    print(f"--- Starting email task for order {order_id} ---")
    # Simulate a time-consuming process
    time.sleep(5) 
    print(f"--- Email sent to {user_email} for order #{order_id} with total ${total_price:.2f} ---")
    return {"status": "success", "message": "Email sent"}