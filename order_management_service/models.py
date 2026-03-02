from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    item_id: str = Field(..., description="Unique identifier for the menu item")
    name: str = Field(..., description="Name of the menu item")
    quantity: int = Field(..., gt=0, description="Quantity of the item ordered")
    price: float = Field(..., gt=0, description="Price per unit of the item")


class OrderStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class Order(BaseModel):
    order_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the order")
    guest_id: str = Field(..., description="Identifier for the guest who placed the order")
    room_number: str = Field(..., description="Room number of the guest")
    items: List[OrderItem] = Field(..., min_length=1, description="List of items in the order")
    total_amount: float = Field(..., gt=0, description="Total cost of the order")
    status: OrderStatus = Field(default=OrderStatus.PENDING, description="Current status of the order")
    delivery_instructions: Optional[str] = Field(None, description="Special delivery instructions")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of order creation")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of last order update")


class OrderCreate(BaseModel):
    guest_id: str
    room_number: str
    items: List[OrderItem]
    delivery_instructions: Optional[str] = None


class OrderUpdate(BaseModel):
    items: Optional[List[OrderItem]] = None
    status: Optional[OrderStatus] = None
    delivery_instructions: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
