"""
管理者向けメニュー管理APIエンドポイント
店舗スタッフが使用するメニューCRUD機能
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.menu import menu_crud
from app.db.database import get_db
from app.db.models import MenuCategory
from app.schemas.menu import MenuCreate, MenuListResponse, MenuResponse, MenuUpdate

router = APIRouter()


@router.get("/", response_model=MenuListResponse)
async def get_admin_menus(
    limit: int = Query(50, ge=1, le=100, description="取得件数"),
    offset: int = Query(0, ge=0, description="開始位置"),
    category: MenuCategory | None = Query(None, description="カテゴリフィルタ"),
    available_only: bool = Query(False, description="販売可能商品のみ取得"),
    db: AsyncSession = Depends(get_db)
) -> MenuListResponse:
    """
    管理者向けメニュー一覧取得

    店舗スタッフ用のメニュー一覧を取得します。
    販売停止中の商品も含めて全商品を取得できます。
    """
    try:
        # データベースからメニューを取得
        menus, total = await menu_crud.get_menus(
            db=db,
            skip=offset,
            limit=limit,
            category=category,
            available_only=available_only
        )

        # レスポンス形式に変換
        menu_responses = [MenuResponse.model_validate(menu) for menu in menus]

        return MenuListResponse(
            items=menu_responses,
            total=total,
            limit=limit,
            offset=offset
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="メニュー一覧の取得に失敗しました"
        ) from None


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_admin_menu_detail(
    menu_id: int,
    db: AsyncSession = Depends(get_db)
) -> MenuResponse:
    """
    管理者向けメニュー詳細取得

    指定されたIDのメニュー詳細を取得します。
    販売停止中の商品も取得できます。
    """
    try:
        # データベースからメニューを取得
        menu = await menu_crud.get_menu_by_id(db=db, menu_id=menu_id)

        if not menu:
            raise HTTPException(
                status_code=404,
                detail="メニューが見つかりません"
            )

        return MenuResponse.model_validate(menu)

    except HTTPException:
        # HTTPExceptionはそのまま再発生
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="メニュー詳細の取得に失敗しました"
        ) from None


@router.post("/", response_model=MenuResponse, status_code=201)
async def create_menu(
    menu_data: MenuCreate,
    db: AsyncSession = Depends(get_db)
) -> MenuResponse:
    """
    メニュー新規作成

    新しいメニューアイテムを作成します。
    """
    try:
        # メニューを作成
        new_menu = await menu_crud.create_menu(db=db, menu_data=menu_data)

        return MenuResponse.model_validate(new_menu)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="メニューの作成に失敗しました"
        ) from None


@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    db: AsyncSession = Depends(get_db)
) -> MenuResponse:
    """
    メニュー更新

    指定されたIDのメニューを更新します。
    """
    try:
        # メニューを更新
        updated_menu = await menu_crud.update_menu(
            db=db,
            menu_id=menu_id,
            menu_data=menu_data
        )

        if not updated_menu:
            raise HTTPException(
                status_code=404,
                detail="メニューが見つかりません"
            )

        return MenuResponse.model_validate(updated_menu)

    except HTTPException:
        # HTTPExceptionはそのまま再発生
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="メニューの更新に失敗しました"
        ) from None


@router.delete("/{menu_id}", status_code=204)
async def delete_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    メニュー削除

    指定されたIDのメニューを削除します。
    """
    try:
        # メニューを削除
        success = await menu_crud.delete_menu(db=db, menu_id=menu_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail="メニューが見つかりません"
            )

    except HTTPException:
        # HTTPExceptionはそのまま再発生
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="メニューの削除に失敗しました"
        ) from None


@router.get("/categories/", response_model=list[str])
async def get_menu_categories() -> list[str]:
    """
    メニューカテゴリ一覧取得

    利用可能なメニューカテゴリの一覧を取得します。
    """
    try:
        # MenuCategoryの全ての値を取得
        categories = [category.value for category in MenuCategory]
        return categories

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="カテゴリ一覧の取得に失敗しました"
        ) from None
