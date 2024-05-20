import json

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_session
from models import Category
from schemas import CategoryCreate, CategoryResponse

router = APIRouter()


@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate, session: AsyncSession = Depends(get_session)
):
    db_category = Category(**category.dict())
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category


@router.get("/", response_model=list[CategoryResponse])
async def read_categories(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Category).offset(skip).limit(limit))
    categories = result.scalars().all()
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
async def read_category(category_id: int, session: AsyncSession = Depends(get_session)):
    db_category = await session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category: CategoryCreate,
    session: AsyncSession = Depends(get_session),
):
    db_category = await session.get(Category, category_id)
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    await session.commit()
    await session.refresh(db_category)
    return db_category


@router.delete("/{category_id}")
async def delete_category(
    category_id: int, session: AsyncSession = Depends(get_session)
):
    db_category = await session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(db_category)
    await session.commit()
    return {"message": "Category deleted successfully"}
