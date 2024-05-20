""" This module contains the API routes for the statistics endpoints.
    Please note that the cache functionality has been commented out in this snippet.
    as it is not required for the task and would require additional setup.
"""

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from database import get_session
from models import Item, Category
from schemas import InventoryStatisticsResponse, LowInventoryItemResponse
from cache import redis_cache

router = APIRouter()


@router.get("/total_stock_value", response_model=float)
async def get_total_stock_value(session: AsyncSession = Depends(get_session)):
    # cached_value = await redis_cache.get("total_stock_value")
    # if cached_value:
    #     return float(cached_value)

    result = await session.execute(select(func.sum(Item.stock)))
    total_stock_value = result.scalar()
    await redis_cache.set("total_stock_value", str(total_stock_value))
    return total_stock_value


@router.get("/low_inventory", response_model=list[LowInventoryItemResponse])
async def get_low_inventory_items(
    threshold: int = 10, session: AsyncSession = Depends(get_session)
):
    # cache_key = f"low_inventory_{threshold}"
    # cached_value = await redis_cache.get(cache_key)
    # if cached_value:
    #     return [LowInventoryItem.parse_raw(item) for item in json.loads(cached_value)]

    result = await session.execute(select(Item).where(Item.stock < threshold))
    items = result.scalars().all()
    await redis_cache.set(cache_key, json.dumps([item.json() for item in items]))
    return [LowInventoryItemResponse.from_orm(item) for item in items]


@router.get("/category_stock", response_model=list[InventoryStatisticsResponse])
async def get_category_stock(session: AsyncSession = Depends(get_session)):
    # cached_value = await redis_cache.get("category_stock")
    # if cached_value:
    #     return [
    #         InventoryStatisticsResponse.parse_raw(item)
    #         for item in json.loads(cached_value)
    #     ]

    result = await session.execute(
        select(Category.name, func.sum(Item.stock)).join(Item).group_by(Category.name)
    )
    category_stats = result.all()
    # await redis_cache.set(
    #     "category_stock",
    #     json.dumps(
    #         [
    #             InventoryStatistics(category_name=name, total_stock=stock).json()
    #             for name, stock in category_stats
    #         ]
    #     ),
    # )
    return [
        InventoryStatistics(category_name=name, total_stock=stock)
        for name, stock in category_stats
    ]
