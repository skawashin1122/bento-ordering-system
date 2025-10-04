"""
APIルーター集約
v1のエンドポイントをまとめる
"""

from fastapi import APIRouter

from app.api.v1.admin import menus as admin_menus
from app.api.v1.endpoints import auth, menus, orders
from app.api.v1.endpoints import orders as admin_orders

api_router = APIRouter()

# 認証関連のエンドポイント
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# メニュー関連のエンドポイント
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])

# 注文関連のエンドポイント
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])

# 管理者向け注文管理のエンドポイント
api_router.include_router(
    admin_orders.router, prefix="/admin/orders", tags=["admin"])

# 管理者向けAPIエンドポイント
api_router.include_router(
    admin_menus.router, prefix="/admin/menus", tags=["admin", "menus"])

# 他のエンドポイントは各担当者が追加
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
