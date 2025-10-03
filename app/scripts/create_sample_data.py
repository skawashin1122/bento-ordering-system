"""
初期データ投入スクリプト
開発用のサンプルメニューデータを作成
"""

import asyncio
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import AsyncSessionLocal
from app.db.models import Menu, MenuCategory, User, UserRole
from app.core.security import get_password_hash


async def create_sample_data():
    """サンプルデータを作成"""
    async with AsyncSessionLocal() as db:
        try:
            # サンプルメニューデータ
            sample_menus = [
                {
                    "name": "唐揚げ弁当",
                    "description": "ジューシーな唐揚げがメインの人気弁当。特製タレでコクと旨味をプラス。",
                    "price": Decimal("500"),
                    "category": MenuCategory.MEAT,
                    "image_url": "https://via.placeholder.com/300x200/e74c3c/ffffff?text=唐揚げ弁当",
                    "is_available": True,
                },
                {
                    "name": "焼肉弁当",
                    "description": "特製タレの焼肉がたっぷり。ボリューム満点で満足度抜群！",
                    "price": Decimal("700"),
                    "category": MenuCategory.MEAT,
                    "image_url": "https://via.placeholder.com/300x200/27ae60/ffffff?text=焼肉弁当",
                    "is_available": True,
                },
                {
                    "name": "鮭弁当",
                    "description": "脂の乗った美味しい鮭。塩加減が絶妙で白いご飯によく合います。",
                    "price": Decimal("600"),
                    "category": MenuCategory.FISH,
                    "image_url": "https://via.placeholder.com/300x200/3498db/ffffff?text=鮭弁当",
                    "is_available": True,
                },
                {
                    "name": "野菜炒め弁当",
                    "description": "新鮮な野菜をシャキシャキに炒めました。ヘルシーで栄養バランス抜群。",
                    "price": Decimal("450"),
                    "category": MenuCategory.VEGETABLE,
                    "image_url": "https://via.placeholder.com/300x200/f39c12/ffffff?text=野菜炒め弁当",
                    "is_available": True,
                },
                {
                    "name": "ハンバーグ弁当",
                    "description": "ジューシーなハンバーグにデミグラスソース。お子様にも大人気！",
                    "price": Decimal("650"),
                    "category": MenuCategory.MEAT,
                    "image_url": "https://via.placeholder.com/300x200/9b59b6/ffffff?text=ハンバーグ弁当",
                    "is_available": True,
                },
                {
                    "name": "海老フライ弁当",
                    "description": "プリプリの海老をサクサクの衣で包みました。タルタルソース付き。",
                    "price": Decimal("750"),
                    "category": MenuCategory.FISH,
                    "image_url": "https://via.placeholder.com/300x200/e67e22/ffffff?text=海老フライ弁当",
                    "is_available": True,
                },
                {
                    "name": "チキン南蛮弁当",
                    "description": "宮崎名物チキン南蛮。甘酢とタルタルソースが絶妙にマッチ！",
                    "price": Decimal("680"),
                    "category": MenuCategory.MEAT,
                    "image_url": "https://via.placeholder.com/300x200/8e44ad/ffffff?text=チキン南蛮弁当",
                    "is_available": True,
                },
                {
                    "name": "サバの味噌煮弁当",
                    "description": "ふっくら煮込んだサバと特製味噌だれ。和食の王道です。",
                    "price": Decimal("580"),
                    "category": MenuCategory.FISH,
                    "image_url": "https://via.placeholder.com/300x200/34495e/ffffff?text=サバ味噌弁当",
                    "is_available": True,
                }
            ]
            
            # メニューデータを挿入
            for menu_data in sample_menus:
                menu = Menu(**menu_data)
                db.add(menu)
            
            # サンプルユーザーデータ
            sample_users = [
                {
                    "email": "customer@example.com",
                    "name": "田中太郎",
                    "hashed_password": get_password_hash("password"),
                    "role": UserRole.CUSTOMER,
                },
                {
                    "email": "store@example.com",
                    "name": "店舗管理者",
                    "hashed_password": get_password_hash("storepass"),
                    "role": UserRole.STORE,
                }
            ]
            
            # ユーザーデータを挿入
            for user_data in sample_users:
                user = User(**user_data)
                db.add(user)
            
            await db.commit()
            print("サンプルデータの作成が完了しました！")
            
        except Exception as e:
            await db.rollback()
            print(f"エラーが発生しました: {e}")
            raise


async def main():
    """メイン実行関数"""
    print("サンプルデータを作成中...")
    await create_sample_data()


if __name__ == "__main__":
    asyncio.run(main())