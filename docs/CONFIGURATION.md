# アプリケーション設定ガイド

## 📋 概要

このアプリケーションは環境変数を使用して設定を管理します。`app/core/config.py` で Pydantic Settings を使用した型安全な設定管理を実装しています。

## 🔧 セットアップ

### 1. 環境変数ファイルの作成

`.env.example` をコピーして `.env` ファイルを作成します：

```bash
cp .env.example .env
```

### 2. 必要な設定値の編集

本番環境では特に以下の設定を必ず変更してください：

```env
# 本番環境では必ず変更！
SECRET_KEY=your-secret-key-change-this-in-production-use-openssl-rand-hex-32

# データベース接続情報
DATABASE_URL=postgresql+asyncpg://your_user:your_password@your_host:5432/your_database
```

## 🔐 セキュリティ関連の設定

### SECRET_KEY の生成

JWTトークンの署名に使用される秘密鍵です。**本番環境では必ず変更してください。**

#### 安全な秘密鍵の生成方法：

```bash
# OpenSSL を使用
openssl rand -hex 32

# Python を使用
python -c "import secrets; print(secrets.token_hex(32))"
```

生成された値を `.env` ファイルの `SECRET_KEY` に設定します。

### JWT設定

```env
# JWTアルゴリズム（通常は変更不要）
ALGORITHM=HS256

# アクセストークンの有効期限（分）
ACCESS_TOKEN_EXPIRE_MINUTES=30

# リフレッシュトークンの有効期限（日）
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## 🗄️ データベース設定

### DATABASE_URL の形式

```
postgresql+asyncpg://ユーザー名:パスワード@ホスト:ポート/データベース名
```

### 開発環境（Docker Compose使用時）

```env
DATABASE_URL=postgresql+asyncpg://bento_user:bento_password@db:5432/bento_ordering
```

### 本番環境の例

```env
DATABASE_URL=postgresql+asyncpg://prod_user:secure_password@db.example.com:5432/bento_prod
```

### テスト環境

テスト用に別のデータベースを使用することを推奨：

```env
TEST_DATABASE_URL=postgresql+asyncpg://bento_user:bento_password@localhost:5432/bento_ordering_test
```

## 🌐 CORS設定

フロントエンドアプリケーションからのアクセスを許可するオリジンを設定します。

### 開発環境

```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000
```

### 本番環境

```env
ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

## 📊 ページネーション設定

```env
# デフォルトのページサイズ
DEFAULT_PAGE_SIZE=20

# 最大ページサイズ（大きすぎる値を防ぐ）
MAX_PAGE_SIZE=100
```

## 🔑 パスワードハッシュ設定

```env
# パスワードハッシュ化スキーマ（bcrypt推奨）
PWD_CONTEXT_SCHEMES=bcrypt

# 非推奨スキーマ
PWD_CONTEXT_DEPRECATED=auto
```

## 📝 使用方法

### Python コードでの設定の使用

```python
from app.core.config import settings

# 設定値にアクセス
app_name = settings.app_name
secret_key = settings.secret_key
database_url = settings.database_url

print(f"アプリケーション名: {app_name}")
print(f"データベースURL: {database_url}")
```

### FastAPI での依存性注入

```python
from fastapi import Depends
from app.core.config import Settings, get_settings

@app.get("/info")
async def get_info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }
```

## 🎯 設定クラスの構造

`app/core/config.py` の `Settings` クラスは以下のセクションで構成されています：

### アプリケーション基本設定

```python
app_name: str = "弁当注文管理システム"
app_version: str = "0.1.0"
debug: bool = False
```

### データベース設定

```python
database_url: str = "postgresql+asyncpg://..."
```

### セキュリティ設定

```python
secret_key: str
algorithm: str = "HS256"
access_token_expire_minutes: int = 30
refresh_token_expire_days: int = 7
```

### CORS設定

```python
allowed_origins: list[str] = ["http://localhost:8000"]
```

### ページネーション設定

```python
default_page_size: int = 20
max_page_size: int = 100
```

## 🔍 設定の検証

アプリケーション起動時に設定が正しく読み込まれるか確認：

```python
python -c "from app.core.config import settings; print(settings.model_dump())"
```

## ⚠️ 重要な注意事項

### セキュリティ

1. **.env ファイルを Git にコミットしない**
   - `.gitignore` に `.env` が含まれていることを確認
   - 本番環境の秘密情報は環境変数として直接設定

2. **SECRET_KEY は絶対に公開しない**
   - GitHub などの公開リポジトリにプッシュしない
   - ログやエラーメッセージに含めない

3. **本番環境では強力なパスワードを使用**
   - データベースパスワードは複雑なものを使用
   - パスワード管理ツールで管理することを推奨

### 環境別の設定

#### 開発環境

```env
DEBUG=True
SECRET_KEY=dev-secret-key-not-for-production
DATABASE_URL=postgresql+asyncpg://bento_user:bento_password@localhost:5432/bento_ordering
```

#### ステージング環境

```env
DEBUG=False
SECRET_KEY=staging-secret-key-generated-securely
DATABASE_URL=postgresql+asyncpg://staging_user:staging_password@staging-db:5432/bento_staging
```

#### 本番環境

```env
DEBUG=False
SECRET_KEY=production-secret-key-generated-securely
DATABASE_URL=postgresql+asyncpg://prod_user:secure_password@prod-db.example.com:5432/bento_prod
ALLOWED_ORIGINS=https://bento-ordering.example.com
```

## 🐳 Docker での使用

### docker-compose.yml での環境変数設定

```yaml
services:
  app:
    env_file:
      - .env
    environment:
      - DATABASE_URL=postgresql+asyncpg://bento_user:bento_password@db:5432/bento_ordering
```

### Docker コンテナ内での確認

```bash
docker-compose exec app python -c "from app.core.config import settings; print(settings.database_url)"
```

## 🔗 関連ファイル

- `.env.example`: 環境変数のテンプレート
- `app/core/config.py`: 設定クラスの定義
- `.gitignore`: `.env` ファイルの除外設定
- `docker-compose.yml`: Docker での環境変数設定

## 📚 参考資料

- [Pydantic Settings ドキュメント](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [FastAPI Configuration ガイド](https://fastapi.tiangolo.com/advanced/settings/)
- [Twelve-Factor App: Config](https://12factor.net/config)
