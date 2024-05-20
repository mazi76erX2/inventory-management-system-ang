import json

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_session
from models import Supplier
from schemas import SupplierCreate, SupplierResponse

router = APIRouter()


@router.post("/", response_model=SupplierResponse)
async def create_supplier(
    supplier: SupplierCreate, session: AsyncSession = Depends(get_session)
):
    db_supplier = Supplier(**supplier.dict())
    session.add(db_supplier)
    await session.commit()
    await session.refresh(db_supplier)
    return db_supplier


@router.get("/", response_model=list[SupplierResponse])
async def read_suppliers(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Supplier).offset(skip).limit(limit))
    suppliers = result.scalars().all()
    return suppliers


@router.get("/{supplier_id}", response_model=SupplierResponse)
async def read_supplier(supplier_id: int, session: AsyncSession = Depends(get_session)):
    db_supplier = await session.get(Supplier, supplier_id)
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(
    supplier_id: int,
    supplier: SupplierCreate,
    session: AsyncSession = Depends(get_session),
):
    db_supplier = await session.get(Supplier, supplier_id)
    for key, value in supplier.dict().items():
        setattr(db_supplier, key, value)
    await session.commit()
    await session.refresh(db_supplier)
    return db_supplier


@router.delete("/{supplier_id}")
async def delete_supplier(supplier_id, session: AsyncSession = Depends(get_session)):
    db_supplier = await session.get(Supplier, supplier_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(db_category)
    await session.commit()
    return {"message": "Category deleted successfully"}
