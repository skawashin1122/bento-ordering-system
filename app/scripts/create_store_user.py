"""店舗管理者アカウント作成スクリプト"""

import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.db.database import AsyncSessionLocal
from app.db.models import User, UserRole

# ロガーの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_store_user(db: AsyncSession):
    """店舗管理者アカウントを作成"""

    # メールアドレスで既存ユーザーを確認
    email = "store@example.com"
    result = await db.execute(select(User).where(User.email == email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        logger.info("Store user already exists")
        return

    # パスワードのハッシュ化
    hashed_password = get_password_hash("password123")

    # 新規ユーザーの作成
    store_user = User(
        email=email,
        name="店舗管理者",
        hashed_password=hashed_password,
        role=UserRole.STORE,
        is_active=True
    )

    db.add(store_user)
    await db.commit()
    logger.info("Store user created successfully")


async def main():
    """メイン処理"""
    async with AsyncSessionLocal() as db:
        await create_store_user(db)

if __name__ == "__main__":
    asyncio.run(main())
