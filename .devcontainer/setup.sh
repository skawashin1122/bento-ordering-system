#!/bin/bash

echo "🚀 Setting up bento-ordering-system development environment..."

# ワークディレクトリ確認
echo "📂 Current directory: $(pwd)"
echo "📋 Workspace contents:"
ls -la /workspace

# 環境変数の確認
echo "📋 Environment check:"
echo "- Python version: $(python --version)"
echo "- Working directory: $(pwd)"

# Pythonパスの設定
export PYTHONPATH="/workspace:/workspace/app:$PYTHONPATH"
echo "- PYTHONPATH: $PYTHONPATH"

# Pythonパスの設定
export PYTHONPATH="/workspace:/workspace/app:$PYTHONPATH"
echo "- PYTHONPATH: $PYTHONPATH"

# 依存関係チェック
echo "� Checking dependencies..."
cd /workspace
if [ -f "requirements.txt" ]; then
    echo "- Found requirements.txt"
else
    echo "- requirements.txt not found"
fi

# データベースの待機（他のコンテナが起動している場合）
echo "⏳ Checking database connection..."
if pg_isready -h db -p 5432 -U bento_user 2>/dev/null; then
    echo "✅ Database is ready"
    
    # Alembic マイグレーション実行
    echo "🗃️ Running database migrations..."
    cd /workspace && alembic upgrade head
else
    echo "⚠️ Database not ready (this is normal if running standalone)"
fi

echo "✅ Development environment setup complete!"
echo ""
echo "🔗 Available services:"
echo "- Web App: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs"
echo "- pgAdmin: http://localhost:8080"
echo ""
echo "📝 Ready to implement Task A: Authentication & User Management!"