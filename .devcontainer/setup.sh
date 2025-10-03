# Codespaces環境セットアップスクリプト
#!/bin/bash

echo "🚀 Setting up bento-ordering-system development environment..."

# 環境変数の確認
echo "📋 Environment check:"
echo "- Python version: $(python --version)"
echo "- Docker version: $(docker --version)"
echo "- Docker Compose version: $(docker-compose --version)"

# データベースの待機
echo "⏳ Waiting for database to be ready..."
until pg_isready -h db -p 5432 -U bentouser; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Alembic マイグレーション実行
echo "🗃️ Running database migrations..."
alembic upgrade head

# 初期データの投入（必要に応じて）
echo "🌱 Setting up initial data..."
python -c "
import asyncio
from app.db.database import get_db
from app.crud.menu import menu_crud
from app.schemas.menu import MenuCreate
from app.db.models import MenuCategory

async def setup_sample_data():
    async for db in get_db():
        # サンプルメニューがない場合のみ作成
        menus, total = await menu_crud.get_menus(db, limit=1)
        if total == 0:
            print('Creating sample menu data...')
            sample_menu = MenuCreate(
                name='サンプル弁当',
                description='開発用サンプルデータです',
                price=500,
                category=MenuCategory.MEAT,
                image_url='https://via.placeholder.com/300x200'
            )
            await menu_crud.create_menu(db, sample_menu)
            print('Sample data created!')
        else:
            print('Sample data already exists.')
        break

asyncio.run(setup_sample_data())
"

echo "✅ Development environment setup complete!"
echo ""
echo "🔗 Available services:"
echo "- Web App: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs"
echo "- pgAdmin: http://localhost:8080"
echo ""
echo "📝 Ready to implement Task A: Authentication & User Management!"