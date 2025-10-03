"""
APIルーター集約
v1のエンドポイントをまとめる
"""

from fastapi import APIRouter

from app.api.v1.endpoints import menus, orders

api_router = APIRouter()

# メニュー関連のエンドポイント
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])

# 注文関連のエンドポイント
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])

# 他のエンドポイントは各担当者が追加
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(admin.router, prefix="/admin", tags=["admin"])