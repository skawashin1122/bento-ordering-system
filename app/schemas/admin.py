"""
管理者用のPydanticスキーマ
店舗管理者向けのAPI用データ構造定義
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field

from app.db.models import OrderStatus


class AdminOrderSummaryResponse(BaseModel):
    """管理者用注文サマリーレスポンススキーマ"""

    id: int = Field(..., description="注文ID")
    user_id: int = Field(..., description="注文者ユーザーID")
    user_name: str = Field(..., description="注文者名")
    user_email: EmailStr = Field(..., description="注文者メールアドレス")
    status: OrderStatus = Field(..., description="注文ステータス")
    total_amount: Decimal = Field(..., description="合計金額（円）")
    delivery_address: str = Field(..., description="配達先住所")
    delivery_time: datetime | None = Field(None, description="希望配達時間")
    notes: str | None = Field(None, description="注文備考")
    items_count: int = Field(..., description="アイテム数")
    created_at: datetime = Field(..., description="注文日時")
    updated_at: datetime = Field(..., description="更新日時")

    class Config:
        from_attributes = True


class AdminOrderDetailResponse(BaseModel):
    """管理者用注文詳細レスポンススキーマ"""

    id: int = Field(..., description="注文詳細ID")
    menu_id: int = Field(..., description="メニューID")
    menu_name: str = Field(..., description="メニュー名")
    quantity: int = Field(..., description="数量")
    unit_price: Decimal = Field(..., description="注文時の単価（円）")
    subtotal: Decimal = Field(..., description="小計（円）")

    class Config:
        from_attributes = True


class AdminOrderResponse(BaseModel):
    """管理者用注文詳細レスポンススキーマ"""

    id: int = Field(..., description="注文ID")
    user_id: int = Field(..., description="注文者ユーザーID")
    user_name: str = Field(..., description="注文者名")
    user_email: EmailStr = Field(..., description="注文者メールアドレス")
    status: OrderStatus = Field(..., description="注文ステータス")
    total_amount: Decimal = Field(..., description="合計金額（円）")
    delivery_address: str = Field(..., description="配達先住所")
    delivery_time: datetime | None = Field(None, description="希望配達時間")
    notes: str | None = Field(None, description="注文備考")
    items: list[AdminOrderDetailResponse] = Field(..., description="注文詳細一覧")
    created_at: datetime = Field(..., description="注文日時")
    updated_at: datetime = Field(..., description="更新日時")

    class Config:
        from_attributes = True


class AdminOrderListResponse(BaseModel):
    """管理者用注文一覧レスポンススキーマ"""

    items: list[AdminOrderSummaryResponse] = Field(..., description="注文一覧")
    total: int = Field(..., ge=0, description="総件数")
    limit: int = Field(..., ge=1, description="取得件数")
    offset: int = Field(..., ge=0, description="開始位置")


class OrderStatusUpdate(BaseModel):
    """注文ステータス更新用スキーマ"""

    status: OrderStatus = Field(..., description="新しい注文ステータス")


class OrderStatusUpdateResponse(BaseModel):
    """注文ステータス更新レスポンススキーマ"""

    id: int = Field(..., description="注文ID")
    status: OrderStatus = Field(..., description="更新された注文ステータス")
    updated_at: datetime = Field(..., description="更新日時")

    class Config:
        from_attributes = True


class PopularMenuStat(BaseModel):
    """人気メニュー統計スキーマ"""

    menu_id: int = Field(..., description="メニューID")
    menu_name: str = Field(..., description="メニュー名")
    order_count: int = Field(..., description="注文数")
    revenue: Decimal = Field(..., description="売上（円）")


class OrderStatistics(BaseModel):
    """注文統計スキーマ"""

    total_orders: int = Field(..., description="総注文数")
    total_revenue: Decimal = Field(..., description="総売上（円）")
    status_breakdown: dict[str, int] = Field(..., description="ステータス別の注文数")
    popular_menus: list[PopularMenuStat] = Field(..., description="人気メニュー一覧")


# 型ヒント用のエイリアス
__all__ = [
    "AdminOrderSummaryResponse",
    "AdminOrderDetailResponse",
    "AdminOrderResponse",
    "AdminOrderListResponse",
    "OrderStatusUpdate",
    "OrderStatusUpdateResponse",
    "PopularMenuStat",
    "OrderStatistics",
]
