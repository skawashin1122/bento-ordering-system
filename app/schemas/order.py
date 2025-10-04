"""
注文関連のPydanticスキーマ
API_SPECS.mdの仕様に基づいたデータ構造定義
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.db.models import OrderStatus


class OrderItemCreate(BaseModel):
    """注文アイテム作成用スキーマ"""
    menu_id: int = Field(..., gt=0, description="メニューID")
    quantity: int = Field(..., gt=0, description="数量")


class OrderCreate(BaseModel):
    """注文作成用スキーマ"""
    items: list[OrderItemCreate] = Field(...,
                                         min_length=1, description="注文アイテム一覧")
    delivery_address: str = Field(..., min_length=1,
                                  max_length=500, description="配達先住所")
    delivery_time: datetime | None = Field(None, description="希望配達時間")
    notes: str | None = Field(None, max_length=1000, description="注文備考")


class OrderDetailResponse(BaseModel):
    """注文詳細レスポンス用スキーマ"""
    id: int = Field(..., description="注文詳細ID")
    menu_id: int = Field(..., description="メニューID")
    menu_name: str = Field(..., description="メニュー名")
    quantity: int = Field(..., description="数量")
    unit_price: Decimal = Field(..., description="注文時の単価（円）")
    subtotal: Decimal = Field(..., description="小計（円）")

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """注文レスポンス用スキーマ"""
    id: int = Field(..., description="注文ID")
    user_id: int = Field(..., description="注文者ユーザーID")
    status: OrderStatus = Field(..., description="注文ステータス")
    total_amount: Decimal = Field(..., description="合計金額（円）")
    delivery_address: str = Field(..., description="配達先住所")
    delivery_time: datetime | None = Field(None, description="希望配達時間")
    notes: str | None = Field(None, description="注文備考")
    items: list[OrderDetailResponse] = Field(..., description="注文詳細一覧")
    created_at: datetime = Field(..., description="注文日時")
    updated_at: datetime = Field(..., description="更新日時")

    class Config:
        from_attributes = True


class OrderSummaryResponse(BaseModel):
    """注文一覧用サマリーレスポンススキーマ"""
    id: int = Field(..., description="注文ID")
    status: OrderStatus = Field(..., description="注文ステータス")
    total_amount: Decimal = Field(..., description="合計金額（円）")
    delivery_address: str = Field(..., description="配達先住所")
    delivery_time: datetime | None = Field(None, description="希望配達時間")
    created_at: datetime = Field(..., description="注文日時")
    items_count: int = Field(..., description="アイテム数")

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """注文一覧レスポンス用スキーマ"""
    items: list[OrderSummaryResponse] = Field(..., description="注文一覧")
    total: int = Field(..., ge=0, description="総件数")
    limit: int = Field(..., ge=1, description="取得件数")
    offset: int = Field(..., ge=0, description="開始位置")


# カート関連のスキーマ
class CartItem(BaseModel):
    """カートアイテムスキーマ"""
    menu_id: int = Field(..., description="メニューID")
    menu_name: str = Field(..., description="メニュー名")
    quantity: int = Field(..., gt=0, description="数量")
    unit_price: Decimal = Field(..., description="単価（円）")
    subtotal: Decimal = Field(..., description="小計（円）")


class CartSummary(BaseModel):
    """カート情報サマリー"""
    items: list[CartItem] = Field(..., description="カートアイテム一覧")
    total_amount: Decimal = Field(..., description="合計金額（円）")
    total_items: int = Field(..., description="総アイテム数")


# 型ヒント用のエイリアス
__all__ = [
    "OrderItemCreate",
    "OrderCreate",
    "OrderDetailResponse",
    "OrderResponse",
    "OrderSummaryResponse",
    "OrderListResponse",
    "CartItem",
    "CartSummary",
]
