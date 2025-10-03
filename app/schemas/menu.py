"""
メニュー関連のPydanticスキーマ
API_SPECS.mdの仕様に基づいたデータ構造定義
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field

from app.db.models import MenuCategory


class MenuBase(BaseModel):
    """メニューの基本スキーマ"""
    name: str = Field(..., min_length=1, max_length=100, description="商品名")
    description: Optional[str] = Field(None, max_length=1000, description="商品説明")
    price: Decimal = Field(..., ge=0, description="価格（円）")
    category: MenuCategory = Field(..., description="カテゴリ")
    image_url: Optional[str] = Field(None, max_length=500, description="商品画像URL")
    is_available: bool = Field(True, description="販売可能フラグ")


class MenuCreate(MenuBase):
    """メニュー作成用スキーマ"""
    pass


class MenuUpdate(BaseModel):
    """メニュー更新用スキーマ"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="商品名")
    description: Optional[str] = Field(None, max_length=1000, description="商品説明")
    price: Optional[Decimal] = Field(None, ge=0, description="価格（円）")
    category: Optional[MenuCategory] = Field(None, description="カテゴリ")
    image_url: Optional[str] = Field(None, max_length=500, description="商品画像URL")
    is_available: Optional[bool] = Field(None, description="販売可能フラグ")


class MenuResponse(MenuBase):
    """メニューレスポンス用スキーマ"""
    id: int = Field(..., description="メニューID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    
    class Config:
        from_attributes = True


class MenuListResponse(BaseModel):
    """メニュー一覧レスポンス用スキーマ"""
    items: List[MenuResponse] = Field(..., description="メニュー一覧")
    total: int = Field(..., ge=0, description="総件数")
    limit: int = Field(..., ge=1, description="取得件数")
    offset: int = Field(..., ge=0, description="開始位置")


# 型ヒント用のエイリアス
__all__ = [
    "MenuBase",
    "MenuCreate",
    "MenuUpdate", 
    "MenuResponse",
    "MenuListResponse",
]