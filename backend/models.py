"""Module for defining the database models."""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class TimestampMixin:
    """Mixin for adding created_at and updated_at timestamps to a model."""

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Item(Base, TimestampMixin):
    """Model for an item in the inventory."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    stock = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

    category = relationship("Category", backref="items", lazy="joined")
    supplier = relationship("Supplier", backref="items", lazy="joined")


class Category(Base, TimestampMixin):
    """Model for a category of items in the inventory."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Supplier(Base, TimestampMixin):
    """Model for a supplier of items in the inventory."""

    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)
