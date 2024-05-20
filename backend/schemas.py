from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(..., description="The item name")
    description: str = Field(None, description="The item description (optional)")
    stock: int = Field(..., description="The current stock level")
    category_id: int = Field(..., description="The ID of the associated category")
    supplier_id: int = Field(..., description="The ID of the associated supplier")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    id: int


class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str = Field(..., description="The category name")


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SupplierBase(BaseModel):
    name: str = Field(..., description="The supplier name")
    contact_info: Optional[str] = Field(
        None, description="The supplier's contact information (optional)"
    )


class SupplierCreate(SupplierBase):
    pass


class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LowInventoryItemBase(BaseModel):
    id: int = Field(..., description="The item name")
    name: str = Field(..., description="The item name")
    description: str = Field(None, description="The item description (optional)")
    stock: int = Field(..., description="The current stock level")
    category_id: int = Field(..., description="The ID of the associated category")
    supplier_id: int = Field(..., description="The ID of the associated supplier")

    class Config:
        from_attributes = True


class LowInventoryItemResponse(LowInventoryItemBase):
    pass


class InventoryStatisticsBase(BaseModel):
    category_name: str = Field(..., description="The category name")
    total_stock: int = Field(..., description="The total stock level for the category")

    class Config:
        from_attributes = True


class InventoryStatisticsResponse(InventoryStatisticsBase):
    pass
