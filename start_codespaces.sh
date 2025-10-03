#!/bin/bash

echo "🚀 弁当注文システム - Codespaces 簡易起動"
echo "============================================"

# プロジェクトルートに移動
cd "$(dirname "$0")"

# 環境テスト
echo "📋 環境確認中..."
python test_codespaces.py

# 依存関係インストール確認
if [ ! -d ".venv" ] && [ -f "requirements.txt" ]; then
    echo "📦 依存関係をインストール中..."
    pip install -r requirements.txt
fi

# 環境変数設定
export PYTHONPATH="$(pwd):$(pwd)/app"
export DATABASE_URL="sqlite:///./test.db"

echo ""
echo "🔗 利用可能なコマンド:"
echo "  開発サーバー起動: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo "  Docker環境起動:   docker-compose up -d"
echo "  環境テスト:       python test_codespaces.py"
echo ""

# 自動起動するかユーザーに確認
read -p "開発サーバーを起動しますか？ (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌟 開発サーバーを起動中..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi