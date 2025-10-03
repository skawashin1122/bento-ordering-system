# 🚀 GitHub Codespaces で始める弁当注文システム開発

## 📋 環境セットアップ

### 1. Codespaces の起動

1. GitHubリポジトリページで `Code` → `Codespaces` → `Create codespace on main`
2. 自動的にPython環境がセットアップされます
3. 依存関係が自動インストールされます

### 2. 開発サーバーの起動

```bash
# 方法1: Docker Compose使用（推奨）
docker-compose up -d

# 方法2: 直接実行（開発用）
export DATABASE_URL="sqlite:///./test.db"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. アクセス確認

- Web App: http://localhost:8000
- API Docs: http://localhost:8000/docs
- pgAdmin: http://localhost:8080 （Docker Compose使用時）

## 🎯 Task A: 認証・ユーザー管理機能

### 実装対象

1. **JWT認証システム**
   - `/api/v1/auth/register` - ユーザー登録
   - `/api/v1/auth/token` - ログイン・トークン取得  
   - `/api/v1/auth/me` - ユーザー情報取得

2. **パスワード管理**
   - bcryptによるハッシュ化
   - 安全なパスワード保存

3. **セキュリティ実装**
   - JWT トークン管理
   - 認証保護エンドポイント

### 📁 ファイル構成

```
app/
├── core/
│   ├── jwt.py          # JWT管理
│   └── security.py     # パスワードハッシュ化
├── schemas/
│   └── auth.py         # 認証用スキーマ
├── crud/
│   └── auth.py         # 認証CRUD操作
├── api/v1/endpoints/
│   └── auth.py         # 認証APIエンドポイント
└── dependencies/
    └── auth.py         # 認証依存関数
```

### 🔧 開発コマンド

```bash
# コードフォーマット
black app/

# 型チェック
mypy app/

# リンティング
ruff check app/

# テスト実行
pytest

# データベースマイグレーション
alembic revision --autogenerate -m "add auth tables"
alembic upgrade head
```

## 🐳 Docker環境

### サービス構成

- **web**: FastAPIアプリケーション (port: 8000)
- **db**: PostgreSQL データベース (port: 5432)  
- **pgadmin**: データベース管理ツール (port: 8080)

### 環境変数

```env
DATABASE_URL=postgresql+asyncpg://bento_user:bento_password@db:5432/bento_ordering
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🎮 開発の開始

1. **認証スキーマから開始**: `app/schemas/auth.py`
2. **JWT管理の実装**: `app/core/jwt.py`
3. **CRUD操作**: `app/crud/auth.py`
4. **APIエンドポイント**: `app/api/v1/endpoints/auth.py`
5. **フロントエンド連携**: `static/js/auth.js`

準備は完了です！Task Aの実装を開始しましょう 🚀