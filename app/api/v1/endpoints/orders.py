"""
注文関連APIエンドポイント
ユーザーの注文作成・履歴取得機能
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.order import order_crud
from app.db.database import get_db
from app.db.models import OrderStatus, User
from app.schemas.order import OrderCreate, OrderListResponse, OrderResponse

router = APIRouter(tags=["orders"])


@router.get("/health")
async def health_check():
    """注文APIヘルスチェック"""
    return {"status": "ok", "message": "注文APIが正常に動作しています"}


async def get_current_user() -> User:
    """
    現在のユーザーを取得（認証機能実装まではモックユーザー）
    TODO: 実際の認証機能と置き換える
    """
    # モックユーザー（ID: 1）を返す
    # 実際の認証実装時にはJWTトークンからユーザー情報を取得
    mock_user = User(id=1, email="test@example.com", name="テストユーザー")
    return mock_user


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
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="注文の処理中にエラーが発生しました"
        )


@router.get("/", response_model=OrderListResponse)
async def get_user_orders(
    page: int = Query(1, ge=1, description="ページ番号"),
    per_page: int = Query(10, ge=1, le=50, description="1ページあたりの件数"),
    status: Optional[OrderStatus] = Query(None, description="注文ステータスでフィルタ"),
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
            status=status
        )
        
        return OrderListResponse(
            orders=orders,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=(total + per_page - 1) // per_page
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="注文履歴の取得中にエラーが発生しました"
        )


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
        raise HTTPException(
            status_code=500,
            detail="注文詳細の取得中にエラーが発生しました"
        )