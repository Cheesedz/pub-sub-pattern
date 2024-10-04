from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Customer(BaseModel):
    customer_id: int
    customer_name: str
    address: str
    email: Optional[str] = None
    phone: Optional[str] = None

class Product(BaseModel):
    product_id: int
    product_name: str
    price: float
    description: Optional[str] = None
    stock_quantity: int

class OrderItem(BaseModel):
    item_id: int
    product: Product
    quantity: int
    total_price: float

class Order(BaseModel):
    order_id: int
    order_date: datetime
    customer: Customer
    items: List[OrderItem]
    total_amount: float
    status: str

class Payment(BaseModel):
    payment_id: int
    order: Order
    payment_date: datetime
    amount_paid: float
    payment_method: str
    payment_status: str

class Package(BaseModel):
    package_id: int
    order_id: int  
    weight: float 
    dimensions: str  
    packaging_type: str 
    shipped_date: datetime
    expected_delivery_date: datetime
    current_status: str  
    tracking_number: Optional[str] = None  
    courier_service: Optional[str] = None  

class DeliveryService(BaseModel):
    delivery_service_id: int
    name: str 
    contact_number: str
    email: Optional[str] = None
    website: Optional[str] = None  
    support_hours: Optional[str] = None 

class Delivery(BaseModel):
    delivery_id: int
    package: Package  
    delivery_service: DeliveryService  
    status: str 
    pickup_date: datetime
    delivery_date: Optional[datetime] = None 
    recipient_name: Optional[str] = None  
    delivery_address: str
    delivery_notes: Optional[str] = None 