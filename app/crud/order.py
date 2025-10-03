"""
注文のCRUD操作
SQLAlchemy 2.0+ asyncio対応
"""

from decimal import Decimal
from typing import List, Optional

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.menu import menu_crud
from app.db.models import Order, OrderDetail, OrderStatus
from app.schemas.order import OrderCreate, OrderItemCreate


class OrderCRUD:
    """注文のCRUD操作クラス"""
    
    @staticmethod
    async def create_order(
        db: AsyncSession,
        order_data: OrderCreate,
        user_id: int
    ) -> Order:
        """
        新規注文を作成
        
        Args:
            db: データベースセッション
            order_data: 注文作成データ
            user_id: 注文者のユーザーID
            
        Returns:
            Order: 作成された注文
            
        Raises:
            ValueError: メニューが見つからない場合やその他のバリデーションエラー
        """
        # 注文アイテムの検証と合計金額計算
        total_amount = Decimal('0')
        order_details_data = []
        
        for item in order_data.items:
            # メニューの存在確認
            menu = await menu_crud.get_menu_by_id(db, item.menu_id)
            if not menu:
                raise ValueError(f"メニューID {item.menu_id} が見つかりません")
            
            if not menu.is_available:
                raise ValueError(f"メニュー「{menu.name}」は現在販売されていません")
            
            # 小計計算
            subtotal = menu.price * item.quantity
            total_amount += subtotal
            
            order_details_data.append({
                'menu_id': item.menu_id,
                'menu': menu,
                'quantity': item.quantity,
                'unit_price': menu.price,
                'subtotal': subtotal
            })
        
        # 注文レコード作成
        db_order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            delivery_address=order_data.delivery_address,
            delivery_time=order_data.delivery_time,
            notes=order_data.notes,
        )
        
        db.add(db_order)
        await db.flush()  # IDを取得するためにflush
        
        # 注文詳細レコード作成
        for detail_data in order_details_data:
            order_detail = OrderDetail(
                order_id=db_order.id,
                menu_id=detail_data['menu_id'],
                quantity=detail_data['quantity'],
                unit_price=detail_data['unit_price'],
                subtotal=detail_data['subtotal'],
            )
            db.add(order_detail)
        
        await db.commit()
        await db.refresh(db_order)
        
        return db_order
    
    @staticmethod
    async def get_user_orders(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        status: Optional[OrderStatus] = None
    ) -> tuple[List[Order], int]:
        """
        ユーザーの注文一覧を取得
        
        Args:
            db: データベースセッション
            user_id: ユーザーID
            skip: スキップ件数
            limit: 取得件数
            status: ステータスフィルタ
            
        Returns:
            tuple[List[Order], int]: (注文一覧, 総件数)
        """
        # ベースクエリを構築
        query = select(Order).where(Order.user_id == user_id)
        count_query = select(func.count(Order.id)).where(Order.user_id == user_id)
        
        # ステータスフィルタ
        if status:
            query = query.where(Order.status == status)
            count_query = count_query.where(Order.status == status)
        
        # 並び順とページネーション
        query = query.order_by(desc(Order.created_at))
        query = query.offset(skip).limit(limit)
        
        # 実行
        result = await db.execute(query)
        orders = result.scalars().all()
        
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0
        
        return list(orders), total
    
    @staticmethod
    async def get_order_by_id(
        db: AsyncSession,
        order_id: int,
        user_id: Optional[int] = None
    ) -> Optional[Order]:
        """
        IDで注文を取得（注文詳細も含む）
        
        Args:
            db: データベースセッション
            order_id: 注文ID
            user_id: ユーザーID（指定した場合、そのユーザーの注文のみ取得）
            
        Returns:
            Optional[Order]: 注文（存在しない場合はNone）
        """
        query = select(Order).options(
            selectinload(Order.order_details).selectinload(OrderDetail.menu)
        ).where(Order.id == order_id)
        
        if user_id is not None:
            query = query.where(Order.user_id == user_id)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_order_status(
        db: AsyncSession,
        order_id: int,
        status: OrderStatus
    ) -> Optional[Order]:
        """
        注文ステータスを更新（管理者用）
        
        Args:
            db: データベースセッション
            order_id: 注文ID
            status: 新しいステータス
            
        Returns:
            Optional[Order]: 更新された注文（存在しない場合はNone）
        """
        query = select(Order).where(Order.id == order_id)
        result = await db.execute(query)
        db_order = result.scalar_one_or_none()
        
        if not db_order:
            return None
        
        db_order.status = status
        await db.commit()
        await db.refresh(db_order)
        
        return db_order
    
    @staticmethod
    async def get_order_items_count(db: AsyncSession, order_id: int) -> int:
        """
        注文のアイテム数を取得
        
        Args:
            db: データベースセッション
            order_id: 注文ID
            
        Returns:
            int: アイテム数
        """
        query = select(func.sum(OrderDetail.quantity)).where(
            OrderDetail.order_id == order_id
        )
        result = await db.execute(query)
        return result.scalar() or 0


# CRUD操作のインスタンス
order_crud = OrderCRUD()