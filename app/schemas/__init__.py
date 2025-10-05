"""
Pydanticスキーマパッケージ
API データ転送用のスキーマ定義
"""

from app.schemas.admin import (
    AdminOrderDetailResponse,
    AdminOrderListResponse,
    AdminOrderResponse,
    AdminOrderSummaryResponse,
    OrderStatistics,
    OrderStatusUpdate,
    OrderStatusUpdateResponse,
    PopularMenuStat,
)
from app.schemas.menu import (
    MenuBase,
    MenuCreate,
    MenuListResponse,
    MenuResponse,
    MenuUpdate,
)
from app.schemas.order import (
    CartItem,
    CartSummary,
    OrderCreate,
    OrderDetailResponse,
    OrderItemCreate,
    OrderListResponse,
    OrderResponse,
    OrderSummaryResponse,
)
from app.schemas.user import (
    Token,
    TokenData,
    UserCreate,
    UserInDB,
    UserLogin,
    UserRegisterResponse,
    UserResponse,
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserInDB",
    "Token",
    "TokenData",
    "UserRegisterResponse",
    # Menu schemas
    "MenuBase",
    "MenuCreate",
    "MenuUpdate",
    "MenuResponse",
    "MenuListResponse",
    # Order schemas
    "OrderItemCreate",
    "OrderCreate",
    "OrderDetailResponse",
    "OrderResponse",
    "OrderSummaryResponse",
    "OrderListResponse",
    "CartItem",
    "CartSummary",
    # Admin schemas
    "AdminOrderSummaryResponse",
    "AdminOrderDetailResponse",
    "AdminOrderResponse",
    "AdminOrderListResponse",
    "OrderStatusUpdate",
    "OrderStatusUpdateResponse",
    "PopularMenuStat",
    "OrderStatistics",
]