from typing import List, Optional
from uuid import UUID

from models import Order, OrderCreate, OrderUpdate, OrderStatus

# In a real application, these would interact with PostgreSQL and MongoDB
# For now, we'll use in-memory dictionaries as mock databases.

mock_orders_db = {}
mock_inventory_db = {
    "item001": {"name": "Club Sandwich", "stock": 10, "price": 12.50},
    "item002": {"name": "Caesar Salad", "stock": 15, "price": 10.00},
    "item003": {"name": "Orange Juice", "stock": 20, "price": 4.00},
}


class OrderService:
    def create_order(self, order_data: OrderCreate) -> Order:
        # Simulate inventory check and deduction
        for item in order_data.items:
            if item.item_id not in mock_inventory_db or mock_inventory_db[item.item_id]["stock"] < item.quantity:
                raise ValueError(f"Item {item.name} (ID: {item.item_id}) is out of stock or insufficient quantity.")
            mock_inventory_db[item.item_id]["stock"] -= item.quantity

        total_amount = sum(item.quantity * item.price for item in order_data.items)
        order = Order(
            **order_data.model_dump(),
            total_amount=total_amount,
            status=OrderStatus.PENDING
        )
        mock_orders_db[str(order.order_id)] = order
        return order

    def get_order(self, order_id: UUID) -> Optional[Order]:
        return mock_orders_db.get(str(order_id))

    def get_all_orders(self) -> List[Order]:
        return list(mock_orders_db.values())

    def update_order(self, order_id: UUID, order_update: OrderUpdate) -> Optional[Order]:
        existing_order = mock_orders_db.get(str(order_id))
        if not existing_order:
            return None

        update_data = order_update.model_dump(exclude_unset=True)
        updated_order = existing_order.model_copy(update=update_data)
        mock_orders_db[str(order_id)] = updated_order
        return updated_order

    def cancel_order(self, order_id: UUID) -> Optional[Order]:
        existing_order = mock_orders_db.get(str(order_id))
        if not existing_order:
            return None

        if existing_order.status == OrderStatus.CANCELLED:
            return existing_order # Already cancelled

        # Simulate inventory replenishment
        for item in existing_order.items:
            if item.item_id in mock_inventory_db:
                mock_inventory_db[item.item_id]["stock"] += item.quantity

        existing_order.status = OrderStatus.CANCELLED
        existing_order.updated_at = datetime.utcnow()
        mock_orders_db[str(order_id)] = existing_order
        return existing_order

    def update_order_status(self, order_id: UUID, new_status: OrderStatus) -> Optional[Order]:
        existing_order = mock_orders_db.get(str(order_id))
        if not existing_order:
            return None
        existing_order.status = new_status
        existing_order.updated_at = datetime.utcnow()
        mock_orders_db[str(order_id)] = existing_order
        return existing_order


class InventoryService:
    def get_item_stock(self, item_id: str) -> Optional[dict]:
        return mock_inventory_db.get(item_id)

    def update_item_stock(self, item_id: str, quantity_change: int) -> Optional[dict]:
        if item_id not in mock_inventory_db:
            return None
        mock_inventory_db[item_id]["stock"] += quantity_change
        return mock_inventory_db[item_id]
