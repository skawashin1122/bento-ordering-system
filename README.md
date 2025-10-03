# 🍱 弁当注文管理システム

**契約駆動開発**によるチーム開発シミュレーション・プロジェクト

## 📋 プロジェクト概要

このプロジェクトは、5人の開発チーム（A, B, C, D, E）が**契約駆動開発 (Contract-Driven Development)**のアプローチで並行開発を進めるための弁当注文管理システムです。

### 🎯 開発アプローチ
- **コアコンセプト**: 契約駆動開発 (Contract-Driven Development)
- **ワークフロー**: GitHub Flow (mainブランチ + フィーチャーブランチ + Pull Request)
- **最重要ドキュメント**: `API_SPECS.md` - 全ての開発の「契約」となります

### 🛠 技術スタック
- **バックエンド**: FastAPI (Python), SQLAlchemy 2.0+ (asyncio + asyncpg), Alembic
- **フロントエンド**: Vanilla JavaScript (ES6+ fetch API), HTML5, CSS3
- **インフラ**: Docker Compose, Poetry
- **コード品質**: Black (フォーマット), Ruff (Lint), MyPy (型チェック)

## 🏗️ プロジェクト構造

```
bento-ordering-system/
├── .devcontainer/          # VS Code開発コンテナ設定
├── app/                    # アプリケーションコード
│   ├── api/v1/endpoints/   # APIエンドポイント
│   ├── core/               # 設定・セキュリティ
│   ├── crud/               # データベース操作
│   ├── db/                 # データベースモデル・接続
│   ├── scripts/            # ユーティリティスクリプト
│   └── main.py             # FastAPIメインアプリ
├── alembic/               # データベースマイグレーション
├── static/                # 静的ファイル
│   ├── css/style.css      # メインスタイルシート
│   └── js/                # JavaScript機能別ファイル
├── templates/             # HTMLテンプレート
├── API_SPECS.md          # 🔥 API仕様書（最重要）
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## 🚀 クイックスタート

### 1. 前提条件
- Docker & Docker Compose
- Poetry（ローカル開発の場合）
- Git

### 2. 環境構築と起動

```bash
# リポジトリをクローン
git clone [repository-url]
cd bento-ordering-system

# 環境変数ファイルをコピー（必要に応じて編集）
cp .env.example .env

# Docker Composeで起動
docker-compose up --build

# データベースマイグレーション（初回のみ）
docker-compose exec web alembic upgrade head
```

### 3. アクセス
- **アプリケーション**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:8080 (admin@example.com / admin)

## 👥 チーム開発フェーズ

### フェーズ 0: 設計と計画 ✅ 完了
- [x] API仕様書 (API_SPECS.md) の策定
- [x] データベースモデルの定義
- [x] 環境構築ファイルの生成
- [x] FastAPIの基本構造作成

### フェーズ 1: 機能コンポーネント並行実装

5人の担当者が以下のタスクを並行開発：

#### 🔐 タスク 1: 担当者A - 認証機能
- **バックエンド**: `/auth/register`, `/auth/token` の実装
- **フロントエンド**: `login.html`, `auth.js` の作成
- **ダミーロジック**: API通信部分はダミーデータで実装

#### 🍱 タスク 2: 担当者B - 公開メニュー機能
- **バックエンド**: `/menus/` (一覧), `/menus/{id}` (詳細) の実装
- **フロントエンド**: `index.html`, `menu.js` の作成
- **ダミーロジック**: JSファイル内にモックデータを直接記述

#### 🛒 タスク 3: 担当者C - カート・注文機能
- **バックエンド**: `/orders/` (注文作成) の実装
- **フロントエンド**: `cart.js` の作成
- **ダミーロジック**: 注文ボタンでアラート表示

#### 📋 タスク 4: 担当者D - 店舗向け商品管理
- **バックエンド**: `/admin/menus/` (メニューCRUD) の実装
- **フロントエンド**: `admin_menu.html`, `admin_menu.js` の作成
- **ダミーロジック**: JS配列データ操作

#### 📊 タスク 5: 担当者E - 店舗向け注文管理
- **バックエンド**: `/admin/orders/` (注文管理) の実装
- **フロントエンド**: `admin_order.html`, `admin_order.js` の作成
- **ダミーロジック**: ステータス変更のUI操作のみ

### フェーズ 2: API結合
各フロントエンドのダミーロジックを実際のAPI呼び出しに置き換え

### フェーズ 3: 最終統合
- 初期データ投入スクリプト作成
- 最終的なREADME更新
- エンドツーエンドテスト

## 📝 開発ガイドライン

### コーディング規約
- **Python**: Black (88文字), Ruff, MyPy完全対応
- **型ヒント**: 必須（FastAPI + SQLAlchemy 2.0+）
- **JavaScript**: ES6+ 機能を積極活用
- **CSS**: BEM記法推奨

### Git ワークフロー
1. mainブランチから新しいフィーチャーブランチを作成
2. 担当機能を実装
3. Pull Request作成
4. コードレビュー
5. mainブランチにマージ

### API開発の契約
- 必ず `API_SPECS.md` の仕様に従って実装
- フロントエンドは仕様書に基づいてダミーデータで先行開発
- バックエンドは仕様書のレスポンス形式を厳守

## 🧪 開発・テスト

### ローカル開発
```bash
# Poetry環境でローカル開発
poetry install
poetry shell

# データベース起動
docker-compose up -d db

# アプリケーション起動（ホットリロード）
uvicorn app.main:app --reload

# データベースマイグレーション
alembic upgrade head

# 新しいマイグレーション作成
alembic revision --autogenerate -m "description"
```

### コード品質チェック
```bash
# フォーマット
black app/
ruff check app/ --fix

# 型チェック
mypy app/

# テスト実行
pytest
```

## 📚 重要ドキュメント

1. **[API_SPECS.md](./API_SPECS.md)** - 最重要：API仕様書
2. **[app/db/models.py](./app/db/models.py)** - データベースモデル定義
3. **[docker-compose.yml](./docker-compose.yml)** - 開発環境設定

## 🔧 トラブルシューティング

### よくある問題

#### Docker関連
```bash
# コンテナの完全リビルド
docker-compose down -v
docker-compose up --build

# ログ確認
docker-compose logs web
docker-compose logs db
```

#### データベース関連
```bash
# マイグレーション状態確認
docker-compose exec web alembic current

# マイグレーション強制実行
docker-compose exec web alembic upgrade head

# データベース初期化（開発環境のみ）
docker-compose exec web python -c "from app.db.database import init_db; import asyncio; asyncio.run(init_db())"
```

#### 依存関係の問題
```bash
# Poetry依存関係の更新
poetry update

# Dockerイメージの再ビルド
docker-compose build --no-cache
```

## 🤝 貢献方法

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. Pull Requestを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 👥 開発チーム

- **担当者A**: 認証機能
- **担当者B**: 公開メニュー機能  
- **担当者C**: カート・注文機能
- **担当者D**: 店舗向け商品管理
- **担当者E**: 店舗向け注文管理

---

**契約駆動開発の成功のカギ**: `API_SPECS.md`を常に最新に保ち、チーム全体が同じ理解を共有することです。