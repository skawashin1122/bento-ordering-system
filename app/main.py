"""
弁当注文管理システム - メインアプリケーション
FastAPI + SQLAlchemy 2.0+ + Vanilla JS
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.api import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    """FastAPIアプリケーションを作成"""

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="弁当注文管理システムのAPI",
        debug=settings.debug,
    )

    # CORS設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 静的ファイル設定
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # APIルーター登録
    app.include_router(api_router, prefix="/api/v1")

    return app


# アプリケーションインスタンス
app = create_application()

# テンプレート設定
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy", "app": settings.app_name}


@app.get("/menus", response_class=HTMLResponse)
async def menus_page(request: Request):
    """メニュー一覧ページ"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/admin/menu", response_class=HTMLResponse)
async def admin_menu_page(request: Request):
    """管理者向けメニュー管理ページ"""
    return templates.TemplateResponse("admin_menu.html", {"request": request})


# この時点では基本的なエンドポイントのみ
# フェーズ1で各担当者がAPIエンドポイントを追加していきます
