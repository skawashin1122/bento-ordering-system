"""
データベース接続設定
SQLAlchemy 2.0+ asyncio対応
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings


# 非同期エンジンを作成
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # デバッグモードでクエリログを出力
    poolclass=NullPool,   # Alembicとの互換性のため
)

# 非同期セッションメーカーを作成
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    データベースセッションを取得する依存性注入関数
    
    Yields:
        AsyncSession: データベースセッション
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    データベースの初期化
    本番環境では使用せず、開発・テスト環境でのみ使用
    """
    from app.db.models import Base
    
    async with engine.begin() as conn:
        # 全テーブルを削除して再作成（注意: 本番環境では絶対に使用しない）
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)