from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Customer(BaseModel):
    customer_id: str | int
    customer_name: str
    address: str
    email: Optional[str] = None
    phone: Optional[str] = None

class Product(BaseModel):
    product_id: str | int
    product_name: str
    price: float
    description: Optional[str] = None
    stock_quantity: int

class OrderItem(BaseModel):
    item_id: str | int
    product: Product
    quantity: int
    total_price: float

class Order(BaseModel):
    order_id: str | int
    order_date: datetime
    customer: Customer
    items: List[OrderItem]
    total_amount: float
    status: str

class Payment(BaseModel):
    payment_id: str | int
    order: Order
    payment_date: datetime
    amount_paid: float
    payment_method: str
    payment_status: str

class Package(BaseModel):
    package_id: str | int
    order_id: str | int  
    weight: float 
    dimensions: str  
    packaging_type: str 
    shipped_date: datetime
    expected_delivery_date: datetime
    current_status: str  
    tracking_number: Optional[str] = None  
    courier_service: Optional[str] = None  

class Delivery(BaseModel):
    delivery_id: str | int
    package: Package  
    status: str 
    pickup_date: datetime
    delivery_date: Optional[datetime] = None 
    recipient_name: Optional[str] = None  
    delivery_address: str
    delivery_notes: Optional[str] = None 