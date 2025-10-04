"""
注文関連APIエンドポイント
ユーザーの注文作成・履歴取得機能
"""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies.auth import get_current_user
from app.crud.order import order_crud
from app.db.database import get_db
from app.db.models import Order, OrderDetail, OrderStatus, User, UserRole
from app.schemas.order import (
    OrderCreate,
    OrderListResponse,
    OrderResponse,
    OrderSummaryResponse,
)

router = APIRouter(tags=["orders"])

# ロガーの設定
logger = logging.getLogger("uvicorn")


@router.get("/admin/orders/", tags=["admin"])
async def get_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: OrderStatus | None = Query(None, description="注文ステータスでフィルタ")
) -> list[OrderSummaryResponse]:
    """
    全ての注文を取得（店舗管理者のみ）

    Args:
        db: データベースセッション
        current_user: 現在のログインユーザー（認証必須）
        status: 注文ステータスでフィルタ

    Returns:
        list[OrderSummaryResponse]: 全注文のリスト

    Raises:
        HTTPException: 
            - 401: 認証エラー
            - 403: 権限エラー（管理者以外）
    """
    if current_user.role != UserRole.STORE:
        raise HTTPException(
            status_code=403,
            detail="この操作を実行する権限がありません"
        )
    try:
        logger.info("Fetching all orders from database")
        stmt = select(Order)
        if status:
            stmt = stmt.where(Order.status == status)
        stmt = stmt.order_by(Order.created_at.desc())

        result = await db.execute(stmt)
        orders = result.scalars().all()
        logger.info(f"Found {len(list(orders))} orders")

        order_details = []
        for order in orders:
            # 注文詳細の取得
            stmt = select(OrderDetail).where(OrderDetail.order_id == order.id)
            result = await db.execute(stmt)
            details = result.scalars().all()

            # 注文情報の構築
            order_info = {
                "id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "total_amount": order.total_amount,
                "delivery_address": order.delivery_address,
                "delivery_time": order.delivery_time,
                "notes": order.notes,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "items": [{
                    "menu_item_id": detail.menu_item_id,
                    "quantity": detail.quantity,
                    "price": detail.price
                } for detail in details]
            }
            order_details.append(OrderSummaryResponse(**order_info))

        return order_details
    except Exception as e:
        logger.exception("An error occurred while fetching orders: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="注文の取得中にエラーが発生しました"
        ) from e
logger = logging.getLogger("uvicorn")


@router.get("/admin/orders/{order_id}", tags=["admin"])
async def get_order_detail(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderResponse:
    """
    指定された注文の詳細を取得（店舗管理者のみ）

    Args:
        order_id: 注文ID
        db: データベースセッション
        current_user: 現在のログインユーザー（認証必須）

    Returns:
        OrderResponse: 注文の詳細情報

    Raises:
        HTTPException:
            - 401: 認証エラー
            - 403: 権限エラー（管理者以外）
            - 404: 注文が見つからない
    """
    if current_user.role != UserRole.STORE:
        raise HTTPException(
            status_code=403,
            detail="この操作を実行する権限がありません"
        )

    try:
        order = await order_crud.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(
                status_code=404,
                detail="指定された注文が見つかりません"
            )
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(
            "An error occurred while fetching order details: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="注文詳細の取得中にエラーが発生しました"
        ) from e


@router.patch("/admin/orders/{order_id}", tags=["admin"])
async def update_order_status(
    order_id: int,
    status: OrderStatus,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderResponse:
    """
    注文のステータスを更新（店舗管理者のみ）

    Args:
        order_id: 注文ID
        status: 新しい注文ステータス
        db: データベースセッション
        current_user: 現在のログインユーザー（認証必須）

    Returns:
        OrderResponse: 更新された注文の詳細

    Raises:
        HTTPException:
            - 401: 認証エラー
            - 403: 権限エラー（管理者以外）
            - 404: 注文が見つからない
    """
    if current_user.role != UserRole.STORE:
        raise HTTPException(
            status_code=403,
            detail="この操作を実行する権限がありません"
        )

    try:
        # 注文の存在確認
        order = await order_crud.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(
                status_code=404,
                detail="指定された注文が見つかりません"
            )

        # ステータスの更新
        order.status = status
        db.add(order)
        await db.commit()
        await db.refresh(order)

        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(
            "An error occurred while updating order status: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="注文ステータスの更新中にエラーが発生しました"
        ) from e


@router.get("/health")
async def health_check():
    """注文APIヘルスチェック"""
    return {"status": "ok", "message": "注文APIが正常に動作しています"}


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    新規注文を作成

    Args:
        order_data: 注文データ
        db: データベースセッション
        current_user: 現在のユーザー

    Returns:
        OrderResponse: 作成された注文の詳細

    Raises:
        HTTPException: 
            - 400: バリデーションエラー
            - 404: メニューが見つからない
    """
    try:
        db_order = await order_crud.create_order(
            db=db,
            order_data=order_data,
            user_id=current_user.id
        )

        # 注文詳細を含む完全な注文情報を再取得
        order_with_details = await order_crud.get_order_by_id(
            db=db,
            order_id=db_order.id,
            user_id=current_user.id
        )

        if not order_with_details:
            raise HTTPException(
                status_code=500,
                detail="注文の作成に失敗しました"
            )

        return order_with_details

    except ValueError as e:
        logger.warning("Validation error: %s", str(e))
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e
    except Exception as e:
        logger.exception("Failed to process order: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="注文の処理中にエラーが発生しました"
        ) from e


@router.get("/", response_model=OrderListResponse)
async def get_user_orders(
    page: int = Query(1, ge=1, description="ページ番号"),
    per_page: int = Query(10, ge=1, le=50, description="1ページあたりの件数"),
    order_status: OrderStatus | None = Query(None, description="注文ステータスでフィルタ"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ユーザーの注文履歴を取得

    Args:
        page: ページ番号
        per_page: 1ページあたりの件数
        status: 注文ステータスフィルタ
        db: データベースセッション
        current_user: 現在のユーザー

    Returns:
        OrderListResponse: 注文一覧
    """
    skip = (page - 1) * per_page

    try:
        orders, total = await order_crud.get_user_orders(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=per_page,
            status=order_status
        )

        # OrderモデルをOrderSummaryResponseに変換
        order_summaries = [
            OrderSummaryResponse(
                id=order.id,
                status=order.status,
                total_amount=order.total_amount,
                delivery_address=order.delivery_address,
                delivery_time=order.delivery_time,
                created_at=order.created_at,
                items_count=await db.scalar(select(func.count()).select_from(OrderDetail).where(OrderDetail.order_id == order.id)) or 0
            ) for order in orders
        ]

        return OrderListResponse(
            items=order_summaries,
            total=total,
            offset=skip,
            limit=per_page
        )

    except Exception as e:
        logger.exception("Failed to fetch user orders: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="注文履歴の取得中にエラーが発生しました"
        ) from e


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_detail(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    注文詳細を取得

    Args:
        order_id: 注文ID
        db: データベースセッション
        current_user: 現在のユーザー

    Returns:
        OrderResponse: 注文詳細

    Raises:
        HTTPException: 404 - 注文が見つからない
    """
    try:
        order = await order_crud.get_order_by_id(
            db=db,
            order_id=order_id,
            user_id=current_user.id
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="注文が見つかりません"
            )

        return order

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to fetch order details: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="注文詳細の取得中にエラーが発生しました"
        ) from e


# -----------------
# 管理者向け注文管理API
# -----------------
# 管理者向け注文管理API
# -----------------

@router.put("/admin/orders/{order_id}/status", tags=["admin"])
async def update_order_status(
    order_id: int,
    order_status: OrderStatus,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """注文のステータスを更新"""
    if current_user.role != UserRole.STORE:
        raise HTTPException(
            status_code=403,
            detail="この操作を実行する権限がありません"
        )

    try:
        order = await order_crud.get_order_by_id(db=db, order_id=order_id)
        if not order:
            raise HTTPException(
                status_code=404,
                detail="注文が見つかりません"
            )

        order.status = order_status
        await db.commit()
        await db.refresh(order)

        return {"message": "注文ステータスが正常に更新されました"}
    except Exception as e:
        logger.exception("Failed to update order status: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="注文ステータスの更新中にエラーが発生しました"
        ) from e
