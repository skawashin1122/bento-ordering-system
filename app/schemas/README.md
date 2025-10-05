# Pydantic スキーマ定義

このディレクトリには、API でデータをやり取りするための Pydantic スキーマが定義されています。

## 📁 ファイル構成

```
app/schemas/
├── __init__.py      # スキーマのエクスポート
├── user.py          # ユーザー・認証関連スキーマ
├── menu.py          # メニュー関連スキーマ
├── order.py         # 注文関連スキーマ
└── admin.py         # 管理者用スキーマ
```

## 🔐 ユーザー・認証スキーマ (`user.py`)

### UserCreate
新規ユーザー登録時に使用するスキーマ。

**フィールド:**
- `email`: メールアドレス（EmailStr）
- `password`: パスワード（8文字以上）
- `name`: ユーザー名（1-100文字）
- `role`: ユーザーロール（customer | store）、デフォルトは customer

**使用例:**
```python
from app.schemas import UserCreate

user_data = UserCreate(
    email="user@example.com",
    password="password123",
    name="田中太郎",
    role="customer"
)
```

### UserResponse
ユーザー情報を返す際のレスポンススキーマ。

**フィールド:**
- `id`: ユーザーID
- `email`: メールアドレス
- `name`: ユーザー名
- `role`: ユーザーロール

### Token
認証トークンのレスポンススキーマ。

**フィールド:**
- `access_token`: JWTアクセストークン
- `token_type`: トークンタイプ（"bearer"）
- `user`: ユーザー情報（UserResponse）

### UserRegisterResponse
ユーザー登録完了時のレスポンス。

**フィールド:**
- `message`: 登録完了メッセージ
- `user`: 登録されたユーザー情報

## 🍱 メニュースキーマ (`menu.py`)

### MenuCreate
新しいメニュー項目を作成する際に使用。

**フィールド:**
- `name`: 商品名（1-100文字）
- `description`: 商品説明（最大1000文字、任意）
- `price`: 価格（0以上の数値）
- `category`: カテゴリ（meat | fish | vegetable | other）
- `image_url`: 商品画像URL（最大500文字、任意）
- `is_available`: 販売可能フラグ（デフォルトTrue）

### MenuResponse
メニュー情報のレスポンス。

**追加フィールド:**
- `id`: メニューID
- `created_at`: 作成日時
- `updated_at`: 更新日時

### MenuListResponse
メニュー一覧のレスポンス。

**フィールド:**
- `items`: メニュー一覧（MenuResponse の配列）
- `total`: 総件数
- `limit`: 取得件数
- `offset`: 開始位置

## 🛒 注文スキーマ (`order.py`)

### OrderItemCreate
注文アイテムを作成する際に使用。

**フィールド:**
- `menu_id`: メニューID（1以上）
- `quantity`: 数量（1以上）

### OrderCreate
新しい注文を作成する際に使用。

**フィールド:**
- `items`: 注文アイテム一覧（OrderItemCreate の配列、最低1件）
- `delivery_address`: 配達先住所（1-500文字）
- `delivery_time`: 希望配達時間（任意）
- `notes`: 注文備考（最大1000文字、任意）

**使用例:**
```python
from app.schemas import OrderCreate, OrderItemCreate

order_data = OrderCreate(
    items=[
        OrderItemCreate(menu_id=1, quantity=2),
        OrderItemCreate(menu_id=2, quantity=1)
    ],
    delivery_address="東京都渋谷区...",
    delivery_time="2024-01-01T18:00:00",
    notes="辛さ控えめでお願いします"
)
```

### OrderResponse
注文情報のレスポンス。

**フィールド:**
- `id`: 注文ID
- `user_id`: 注文者ユーザーID
- `status`: 注文ステータス
- `total_amount`: 合計金額
- `delivery_address`: 配達先住所
- `delivery_time`: 希望配達時間
- `notes`: 注文備考
- `items`: 注文詳細一覧
- `created_at`: 注文日時
- `updated_at`: 更新日時

### CartItem / CartSummary
カート機能用のスキーマ。

## 🏪 管理者用スキーマ (`admin.py`)

### AdminOrderResponse
管理者用の注文詳細レスポンス。顧客用のレスポンスに加えて、注文者情報を含む。

**追加フィールド:**
- `user_name`: 注文者名
- `user_email`: 注文者メールアドレス

### OrderStatusUpdate
注文ステータスを更新する際に使用。

**フィールド:**
- `status`: 新しいステータス（pending | preparing | ready | delivered | cancelled）

### OrderStatistics
注文統計情報。

**フィールド:**
- `total_orders`: 総注文数
- `total_revenue`: 総売上
- `status_breakdown`: ステータス別注文数
- `popular_menus`: 人気メニュー一覧

## 🎯 使用方法

### インポート

```python
# 個別にインポート
from app.schemas.user import UserCreate, UserResponse
from app.schemas.menu import MenuCreate, MenuResponse
from app.schemas.order import OrderCreate, OrderResponse

# まとめてインポート
from app.schemas import (
    UserCreate,
    UserResponse,
    MenuCreate,
    OrderCreate,
)
```

### バリデーション

Pydantic はデータを自動的にバリデーションします：

```python
from app.schemas import UserCreate

# ✅ 正常なデータ
user = UserCreate(
    email="user@example.com",
    password="password123",
    name="田中太郎"
)

# ❌ エラー: メールアドレスが不正
user = UserCreate(
    email="invalid-email",  # ValidationError が発生
    password="password123",
    name="田中太郎"
)

# ❌ エラー: パスワードが短すぎる
user = UserCreate(
    email="user@example.com",
    password="short",  # ValidationError が発生（8文字未満）
    name="田中太郎"
)
```

### データベースモデルとの変換

```python
from app.db.models import User
from app.schemas import UserResponse

# データベースモデルから Pydantic スキーマへ
user_db = User(id=1, email="user@example.com", name="田中太郎", role="customer")
user_response = UserResponse.from_orm(user_db)

# または model_validate を使用
user_response = UserResponse.model_validate(user_db)
```

## 📝 設計原則

1. **API仕様との整合性**: すべてのスキーマは `API_SPECS.md` の仕様に基づいています
2. **型安全性**: Pydantic v2 を使用し、厳格な型チェックを実施
3. **バリデーション**: フィールドレベルでのバリデーションルールを定義
4. **ドキュメント**: すべてのフィールドに `description` を付与
5. **再利用性**: 共通のスキーマを基底クラスとして定義

## 🔗 関連ファイル

- `app/db/models.py`: データベースモデル定義
- `app/core/config.py`: アプリケーション設定
- `API_SPECS.md`: API仕様書
