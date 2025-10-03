"""
メニューのCRUD操作
SQLAlchemy 2.0+ asyncio対応
"""

from typing import List, Optional

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Menu, MenuCategory
from app.schemas.menu import MenuCreate, MenuUpdate


class MenuCRUD:
    """メニューのCRUD操作クラス"""
    
    @staticmethod
    async def get_menus(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
        category: Optional[MenuCategory] = None,
        available_only: bool = True
    ) -> tuple[List[Menu], int]:
        """
        メニュー一覧を取得
        
        Args:
            db: データベースセッション
            skip: スキップ件数
            limit: 取得件数
            category: カテゴリフィルタ
            available_only: 販売可能商品のみ取得するかどうか
            
        Returns:
            tuple[List[Menu], int]: (メニュー一覧, 総件数)
        """
        # ベースクエリを構築
        query = select(Menu)
        count_query = select(func.count(Menu.id))
        
        # フィルタ条件を追加
        if available_only:
            query = query.where(Menu.is_available == True)
            count_query = count_query.where(Menu.is_available == True)
        
        if category:
            query = query.where(Menu.category == category)
            count_query = count_query.where(Menu.category == category)
        
        # 並び順とページネーション
        query = query.order_by(desc(Menu.created_at))
        query = query.offset(skip).limit(limit)
        
        # 実行
        result = await db.execute(query)
        menus = result.scalars().all()
        
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0
        
        return list(menus), total
    
    @staticmethod
    async def get_menu_by_id(db: AsyncSession, menu_id: int) -> Optional[Menu]:
        """
        IDでメニューを取得
        
        Args:
            db: データベースセッション
            menu_id: メニューID
            
        Returns:
            Optional[Menu]: メニュー（存在しない場合はNone）
        """
        query = select(Menu).where(Menu.id == menu_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_menu(db: AsyncSession, menu_data: MenuCreate) -> Menu:
        """
        新規メニューを作成
        
        Args:
            db: データベースセッション
            menu_data: メニュー作成データ
            
        Returns:
            Menu: 作成されたメニュー
        """
        db_menu = Menu(
            name=menu_data.name,
            description=menu_data.description,
            price=menu_data.price,
            category=menu_data.category,
            image_url=menu_data.image_url,
            is_available=menu_data.is_available,
        )
        
        db.add(db_menu)
        await db.commit()
        await db.refresh(db_menu)
        
        return db_menu
    
    @staticmethod
    async def update_menu(
        db: AsyncSession, 
        menu_id: int, 
        menu_data: MenuUpdate
    ) -> Optional[Menu]:
        """
        メニューを更新
        
        Args:
            db: データベースセッション
            menu_id: メニューID
            menu_data: 更新データ
            
        Returns:
            Optional[Menu]: 更新されたメニュー（存在しない場合はNone）
        """
        query = select(Menu).where(Menu.id == menu_id)
        result = await db.execute(query)
        db_menu = result.scalar_one_or_none()
        
        if not db_menu:
            return None
        
        # 更新データを適用（Noneでない値のみ）
        update_data = menu_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_menu, field, value)
        
        await db.commit()
        await db.refresh(db_menu)
        
        return db_menu
    
    @staticmethod
    async def delete_menu(db: AsyncSession, menu_id: int) -> bool:
        """
        メニューを削除
        
        Args:
            db: データベースセッション
            menu_id: メニューID
            
        Returns:
            bool: 削除成功かどうか
        """
        query = select(Menu).where(Menu.id == menu_id)
        result = await db.execute(query)
        db_menu = result.scalar_one_or_none()
        
        if not db_menu:
            return False
        
        await db.delete(db_menu)
        await db.commit()
        
        return True


# CRUD操作のインスタンス
menu_crud = MenuCRUD()