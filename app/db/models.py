"""
弁当注文管理システム - データベースモデル定義

SQLAlchemy 2.0+ + asyncio対応
MyPy完全対応のため、全ての型ヒントを記述
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """全てのモデルの基底クラス"""
    pass


class UserRole(str, Enum):
    """ユーザーロール列挙型"""
    CUSTOMER = "customer"
    STORE = "store"


class OrderStatus(str, Enum):
    """注文ステータス列挙型"""
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class MenuCategory(str, Enum):
    """メニューカテゴリ列挙型"""
    MEAT = "meat"
    FISH = "fish"
    VEGETABLE = "vegetable"
    OTHER = "other"


class User(Base):
    """ユーザーモデル（顧客・店舗管理者の両方を管理）"""
    
    __tablename__ = "users"
    
    # 主キー
    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True,
        comment="ユーザーID"
    )
    
    # 基本情報
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="メールアドレス（ログインID）"
    )
    
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="ユーザー名"
    )
    
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="ハッシュ化されたパスワード"
    )
    
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.CUSTOMER,
        comment="ユーザーロール（顧客 or 店舗管理者）"
    )
    
    # 状態管理
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="アカウント有効フラグ"
    )
    
    # タイムスタンプ
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="作成日時"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新日時"
    )
    
    # リレーション
    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"


class Menu(Base):
    """メニューモデル（弁当商品情報）"""
    
    __tablename__ = "menus"
    
    # 主キー
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="メニューID"
    )
    
    # 商品情報
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="商品名"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="商品説明"
    )
    
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 0),  # 小数点なし、最大10桁
        nullable=False,
        comment="価格（円）"
    )
    
    category: Mapped[MenuCategory] = mapped_column(
        SQLEnum(MenuCategory),
        nullable=False,
        default=MenuCategory.OTHER,
        comment="カテゴリ"
    )
    
    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="商品画像URL"
    )
    
    # 状態管理
    is_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="販売可能フラグ"
    )
    
    # タイムスタンプ
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="作成日時"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新日時"
    )
    
    # リレーション
    order_details: Mapped[List["OrderDetail"]] = relationship(
        "OrderDetail",
        back_populates="menu",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Menu(id={self.id}, name='{self.name}', price={self.price})>"


class Order(Base):
    """注文モデル"""
    
    __tablename__ = "orders"
    
    # 主キー
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="注文ID"
    )
    
    # 外部キー
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="注文者ユーザーID"
    )
    
    # 注文情報
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus),
        nullable=False,
        default=OrderStatus.PENDING,
        index=True,
        comment="注文ステータス"
    )
    
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 0),  # 小数点なし、最大10桁
        nullable=False,
        comment="合計金額（円）"
    )
    
    # 配達情報
    delivery_address: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="配達先住所"
    )
    
    delivery_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="希望配達時間"
    )
    
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="注文備考"
    )
    
    # タイムスタンプ
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="注文日時"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新日時"
    )
    
    # リレーション
    user: Mapped["User"] = relationship(
        "User",
        back_populates="orders"
    )
    
    order_details: Mapped[List["OrderDetail"]] = relationship(
        "OrderDetail",
        back_populates="order",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Order(id={self.id}, user_id={self.user_id}, status='{self.status}', total={self.total_amount})>"


class OrderDetail(Base):
    """注文詳細モデル（注文内の各商品）"""
    
    __tablename__ = "order_details"
    
    # 主キー
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="注文詳細ID"
    )
    
    # 外部キー
    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="注文ID"
    )
    
    menu_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("menus.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="メニューID"
    )
    
    # 注文詳細情報
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="数量"
    )
    
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 0),  # 小数点なし、最大10桁
        nullable=False,
        comment="注文時の単価（円）"
    )
    
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 0),  # 小数点なし、最大10桁
        nullable=False,
        comment="小計（円）= quantity × unit_price"
    )
    
    # タイムスタンプ
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="作成日時"
    )
    
    # リレーション
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="order_details"
    )
    
    menu: Mapped["Menu"] = relationship(
        "Menu",
        back_populates="order_details"
    )
    
    def __repr__(self) -> str:
        return f"<OrderDetail(id={self.id}, order_id={self.order_id}, menu_id={self.menu_id}, qty={self.quantity})>"


# 型ヒント用の追加定義（MyPy対応）
__all__ = [
    "Base",
    "User",
    "Menu", 
    "Order",
    "OrderDetail",
    "UserRole",
    "OrderStatus",
    "MenuCategory",
]