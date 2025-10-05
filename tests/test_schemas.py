"""
Pydanticスキーマのテスト
データ構造のバリデーションとシリアライゼーションを検証
"""

from decimal import Decimal
from datetime import datetime

import pytest
from pydantic import ValidationError

from app.db.models import MenuCategory, OrderStatus, UserRole
from app.schemas.admin import (
    AdminOrderResponse,
    OrderStatistics,
    OrderStatusUpdate,
    PopularMenuStat,
)
from app.schemas.menu import MenuCreate, MenuResponse, MenuUpdate
from app.schemas.order import CartItem, OrderCreate, OrderItemCreate, OrderResponse
from app.schemas.user import (
    Token,
    UserCreate,
    UserLogin,
    UserRegisterResponse,
    UserResponse,
)


class TestUserSchemas:
    """ユーザースキーマのテスト"""

    def test_user_create_valid(self):
        """正常なユーザー作成データ"""
        user = UserCreate(
            email="test@example.com",
            password="password123",
            name="Test User",
            role=UserRole.CUSTOMER,
        )
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.name == "Test User"
        assert user.role == UserRole.CUSTOMER

    def test_user_create_default_role(self):
        """デフォルトのロール（customer）"""
        user = UserCreate(
            email="test@example.com", password="password123", name="Test User"
        )
        assert user.role == UserRole.CUSTOMER

    def test_user_create_invalid_email(self):
        """無効なメールアドレス"""
        with pytest.raises(ValidationError):
            UserCreate(email="invalid-email", password="password123", name="Test User")

    def test_user_create_short_password(self):
        """短すぎるパスワード"""
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com", password="short", name="Test User")

    def test_user_response(self):
        """ユーザーレスポンススキーマ"""
        user = UserResponse(
            id=1,
            email="test@example.com",
            name="Test User",
            role=UserRole.CUSTOMER,
        )
        assert user.id == 1
        assert user.email == "test@example.com"

    def test_token_with_user(self):
        """ユーザー情報を含むトークン"""
        user = UserResponse(
            id=1,
            email="test@example.com",
            name="Test User",
            role=UserRole.CUSTOMER,
        )
        token = Token(access_token="test-token", token_type="bearer", user=user)
        assert token.access_token == "test-token"
        assert token.user.name == "Test User"

    def test_user_login(self):
        """ログインスキーマ"""
        login = UserLogin(email="test@example.com", password="password123")
        assert login.email == "test@example.com"
        assert login.password == "password123"


class TestMenuSchemas:
    """メニュースキーマのテスト"""

    def test_menu_create_valid(self):
        """正常なメニュー作成データ"""
        menu = MenuCreate(
            name="唐揚げ弁当",
            description="美味しい弁当",
            price=Decimal("500"),
            category=MenuCategory.MEAT,
            is_available=True,
        )
        assert menu.name == "唐揚げ弁当"
        assert menu.price == Decimal("500")
        assert menu.category == MenuCategory.MEAT

    def test_menu_create_negative_price(self):
        """負の価格"""
        with pytest.raises(ValidationError):
            MenuCreate(
                name="Test Menu",
                price=Decimal("-100"),
                category=MenuCategory.MEAT,
            )

    def test_menu_update_partial(self):
        """部分的な更新"""
        update = MenuUpdate(price=Decimal("600"))
        assert update.price == Decimal("600")
        assert update.name is None

    def test_menu_response(self):
        """メニューレスポンス"""
        menu = MenuResponse(
            id=1,
            name="唐揚げ弁当",
            price=Decimal("500"),
            category=MenuCategory.MEAT,
            is_available=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        assert menu.id == 1
        assert menu.name == "唐揚げ弁当"


class TestOrderSchemas:
    """注文スキーマのテスト"""

    def test_order_item_create_valid(self):
        """正常な注文アイテム"""
        item = OrderItemCreate(menu_id=1, quantity=2)
        assert item.menu_id == 1
        assert item.quantity == 2

    def test_order_item_create_invalid_quantity(self):
        """無効な数量（0以下）"""
        with pytest.raises(ValidationError):
            OrderItemCreate(menu_id=1, quantity=0)

        with pytest.raises(ValidationError):
            OrderItemCreate(menu_id=1, quantity=-1)

    def test_order_create_valid(self):
        """正常な注文作成"""
        order = OrderCreate(
            items=[
                OrderItemCreate(menu_id=1, quantity=2),
                OrderItemCreate(menu_id=2, quantity=1),
            ],
            delivery_address="東京都渋谷区",
            notes="よろしくお願いします",
        )
        assert len(order.items) == 2
        assert order.delivery_address == "東京都渋谷区"

    def test_order_create_empty_items(self):
        """空の注文アイテム（エラー）"""
        with pytest.raises(ValidationError):
            OrderCreate(items=[], delivery_address="東京都渋谷区")

    def test_cart_item(self):
        """カートアイテム"""
        cart_item = CartItem(
            menu_id=1,
            menu_name="唐揚げ弁当",
            quantity=2,
            unit_price=Decimal("500"),
            subtotal=Decimal("1000"),
        )
        assert cart_item.quantity == 2
        assert cart_item.subtotal == Decimal("1000")


class TestAdminSchemas:
    """管理者スキーマのテスト"""

    def test_order_status_update(self):
        """注文ステータス更新"""
        update = OrderStatusUpdate(status=OrderStatus.PREPARING)
        assert update.status == OrderStatus.PREPARING

    def test_popular_menu_stat(self):
        """人気メニュー統計"""
        stat = PopularMenuStat(
            menu_id=1,
            menu_name="唐揚げ弁当",
            order_count=45,
            revenue=Decimal("22500"),
        )
        assert stat.menu_id == 1
        assert stat.order_count == 45
        assert stat.revenue == Decimal("22500")

    def test_order_statistics(self):
        """注文統計"""
        stats = OrderStatistics(
            total_orders=150,
            total_revenue=Decimal("125000"),
            status_breakdown={"pending": 10, "delivered": 130},
            popular_menus=[
                PopularMenuStat(
                    menu_id=1,
                    menu_name="唐揚げ弁当",
                    order_count=45,
                    revenue=Decimal("22500"),
                )
            ],
        )
        assert stats.total_orders == 150
        assert stats.total_revenue == Decimal("125000")
        assert len(stats.popular_menus) == 1
