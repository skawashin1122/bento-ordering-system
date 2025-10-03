# GitHub Codespaces Development Environment

## 🚀 Quick Start

この環境は GitHub Codespaces で弁当注文システムの開発をするために最適化されています。

### 🛠️ Codespaces起動手順

1. **GitHub リポジトリで Codespaces を起動**
   ```
   Code → Codespaces → Create codespace on main
   ```

2. **自動セットアップの確認**
   - 環境構築スクリプトが自動実行されます
   - 必要な拡張機能が自動インストールされます
   - ワークスペースは `/workspace` にマウントされます

3. **開発サーバー起動**
   ```bash
   # Docker Compose でサービス起動
   docker-compose up -d
   
   # または、Pythonを直接実行
   cd /workspace
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### 利用可能なサービス

| サービス | ポート | URL | 説明 |
|---------|-------|-----|-----|
| Web App | 8000 | http://localhost:8000 | FastAPI アプリケーション |
| API Docs | 8000 | http://localhost:8000/docs | Swagger UI |
| PostgreSQL | 5432 | localhost:5432 | データベース |
| pgAdmin | 8080 | http://localhost:8080 | DB管理ツール |

### 開発用コマンド

```bash
# アプリケーション起動
docker-compose up -d

# ログ確認
docker-compose logs -f web

# データベースマイグレーション
docker-compose exec web alembic upgrade head

# 新しいマイグレーション作成
docker-compose exec web alembic revision --autogenerate -m "description"

# テスト実行
docker-compose exec web pytest

# コードフォーマット
docker-compose exec web black app/
docker-compose exec web ruff check app/

# 型チェック
docker-compose exec web mypy app/
```

## 📋 Task A: 認証・ユーザー管理機能の実装

### 実装対象

1. **JWT認証システム**
   - ユーザー登録・ログイン
   - アクセストークン・リフレッシュトークン
   - パスワードハッシュ化

2. **ユーザー管理**
   - プロファイル管理
   - パスワード変更
   - アカウント削除

3. **認証保護**
   - エンドポイント保護
   - ロールベースアクセス制御
   - セッション管理

### 開発フロー

1. 認証用スキーマ作成 (`app/schemas/auth.py`)
2. 認証CRUD操作実装 (`app/crud/auth.py`)
3. JWT管理モジュール (`app/core/jwt.py`)
4. 認証APIエンドポイント (`app/api/v1/endpoints/auth.py`)
5. フロントエンド認証機能 (`static/js/auth.js`)

## 🔧 トラブルシューティング

### ポートが使用できない場合

```bash
# プロセス確認
lsof -i :8000

# Docker コンテナ再起動
docker-compose restart
```

### データベース接続エラー

```bash
# データベースコンテナ確認
docker-compose ps db

# データベースログ確認
docker-compose logs db
```

### 依存関係の問題

```bash
# コンテナ再ビルド
docker-compose up -d --build

# 依存関係再インストール
docker-compose exec web pip install -r requirements.txt
```

## 📚 参考リソース

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [JWT.io](https://jwt.io/) - JWT デバッグツール

## 🔐 環境変数

必要な環境変数は `.env` ファイルで管理されています：

```env
# Database
POSTGRES_USER=bentouser
POSTGRES_PASSWORD=bentopass
POSTGRES_DB=bentodb

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```