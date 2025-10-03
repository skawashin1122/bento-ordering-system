#!/bin/bash

echo "🚀 Setting up bento-ordering-system Codespaces environment..."

# ワークディレクトリに移動
cd /workspace

# Python環境セットアップ
echo "🐍 Setting up Python environment..."
pip install --upgrade pip
pip install -r requirements.txt

# 環境変数の確認
echo "📋 Environment check:"
echo "- Python version: $(python --version)"
echo "- Working directory: $(pwd)"

# Docker Compose でサービス起動
echo "🐳 Starting services with Docker Compose..."
docker-compose up -d

# データベースの準備が整うまで待機
echo "⏳ Waiting for database to be ready..."
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U bento_user >/dev/null 2>&1; then
        echo "✅ Database is ready!"
        break
    fi
    echo "Waiting for PostgreSQL... ($i/30)"
    sleep 2
done

# データベースマイグレーション
echo "🗃️ Running database migrations..."
docker-compose exec -T web alembic upgrade head || echo "⚠️ Migration will run when web service starts"

echo "✅ Codespaces environment setup complete!"
echo ""
echo "🔗 Available services:"
echo "- Web App: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs" 
echo "- pgAdmin: http://localhost:8080"
echo ""
echo "📝 Ready to implement Task A: Authentication & User Management!"
echo ""
echo "💡 Quick start commands:"
echo "  docker-compose logs -f web    # View web logs"
echo "  docker-compose ps             # Check service status"
echo "  uvicorn app.main:app --reload # Run development server"