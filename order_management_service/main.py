from typing import List
from uuid import UUID

from fastapi import FastAPI, HTTPException, status
from models import Order, OrderCreate, OrderUpdate, OrderStatus
from services import OrderService

app = FastAPI(
    title="Order Management Service",
    description="API for managing room service orders.",
    version="1.0.0",
)

order_service = OrderService()


@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order_create: OrderCreate):
    """Create a new room service order."""
    try:
        order = order_service.create_order(order_create)
        return order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/orders", response_model=List[Order])
async def get_all_orders():
    """Retrieve a list of all room service orders."""
    return order_service.get_all_orders()


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: UUID):
    """Retrieve details of a specific room service order."""
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: UUID, order_update: OrderUpdate):
    """Update an existing room service order."""
    updated_order = order_service.update_order(order_id, order_update)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated_order


@app.patch("/orders/{order_id}/status", response_model=Order)
async def update_order_status(order_id: UUID, new_status: OrderStatus):
    """Update the status of a room service order."""
    updated_order = order_service.update_order_status(order_id, new_status)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated_order


@app.delete("/orders/{order_id}", response_model=Order)
async def cancel_order(order_id: UUID):
    """Cancel a room service order."""
    cancelled_order = order_service.cancel_order(order_id)
    if not cancelled_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return cancelled_order
