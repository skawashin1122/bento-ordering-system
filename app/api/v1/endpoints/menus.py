"""
公開メニューAPIエンドポイント
API_SPECS.mdの仕様に基づく実装
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.menu import menu_crud
from app.db.database import get_db
from app.db.models import MenuCategory
from app.schemas.menu import MenuListResponse, MenuResponse

router = APIRouter()


@router.get("/", response_model=MenuListResponse)
async def get_menus(
    limit: int = Query(50, ge=1, le=100, description="取得件数"),
    offset: int = Query(0, ge=0, description="開始位置"),
    category: Optional[MenuCategory] = Query(None, description="カテゴリフィルタ"),
    db: AsyncSession = Depends(get_db)
) -> MenuListResponse:
    """
    メニュー一覧取得
    
    公開メニューの一覧を取得します。
    販売可能な商品のみ返却されます。
    """
    try:
        # データベースからメニューを取得
        menus, total = await menu_crud.get_menus(
            db=db,
            skip=offset,
            limit=limit,
            category=category,
            available_only=True  # 公開メニューは販売可能商品のみ
        )
        
        # レスポンス形式に変換
        menu_responses = [MenuResponse.model_validate(menu) for menu in menus]
        
        return MenuListResponse(
            items=menu_responses,
            total=total,
            limit=limit,
            offset=offset
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="メニュー一覧の取得に失敗しました"
        )


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu_detail(
    menu_id: int,
    db: AsyncSession = Depends(get_db)
) -> MenuResponse:
    """
    メニュー詳細取得
    
    指定されたIDのメニュー詳細を取得します。
    """
    try:
        # データベースからメニューを取得
        menu = await menu_crud.get_menu_by_id(db=db, menu_id=menu_id)
        
        if not menu:
            raise HTTPException(
                status_code=404,
                detail="メニューが見つかりません"
            )
        
        # 販売停止商品の場合は公開しない
        if not menu.is_available:
            raise HTTPException(
                status_code=404,
                detail="メニューが見つかりません"
            )
        
        return MenuResponse.model_validate(menu)
        
    except HTTPException:
        # HTTPExceptionはそのまま再発生
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="メニュー詳細の取得に失敗しました"
        )