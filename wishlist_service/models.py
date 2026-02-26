from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from .database import Base

class WishlistItemStatus(str, enum.Enum):
    active = "active"
    moved_to_cart = "moved_to_cart"
    out_of_stock = "out_of_stock"
    unavailable = "unavailable"

class Wishlist(Base):
    __tablename__ = "wishlists"

    wishlist_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), onupdate=func.now())

    items = relationship("WishlistItem", back_populates="wishlist", cascade="all, delete-orphan")

class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wishlist_id = Column(UUID(as_uuid=True), ForeignKey("wishlists.wishlist_id"), nullable=False)
    product_id = Column(String, nullable=False, index=True)
    quantity = Column(Integer, default=1)
    added_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(WishlistItemStatus), default=WishlistItemStatus.active, nullable=False)

    wishlist = relationship("Wishlist", back_populates="items")
