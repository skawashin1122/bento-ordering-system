# 弁当注文管理システム API仕様書

## 📋 概要
この文書は弁当注文管理システムの全APIエンドポイントを定義する「契約書」です。
チーム開発において、バックエンドとフロントエンドの実装者が並行開発できるよう、明確なインターフェースを規定します。

## 🏗️ 基本情報
- **ベースURL**: `http://localhost:8000`
- **APIバージョン**: v1 (`/api/v1/`)
- **認証方式**: JWT Bearer Token
- **Content-Type**: `application/json`

---

## 🔐 認証エンドポイント（担当者A）

### POST /api/v1/auth/register
新規ユーザー登録

**リクエスト**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "ユーザー名",
  "role": "customer"  // "customer" | "store"
}
```

**レスポンス (201 Created)**
```json
{
  "message": "ユーザーが正常に登録されました",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "ユーザー名",
    "role": "customer"
  }
}
```

**エラーレスポンス (400 Bad Request)**
```json
{
  "detail": "このメールアドレスは既に登録されています"
}
```

### POST /api/v1/auth/token
ログイン・トークン取得

**リクエスト**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**レスポンス (200 OK)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "ユーザー名",
    "role": "customer"
  }
}
```

**エラーレスポンス (401 Unauthorized)**
```json
{
  "detail": "メールアドレスまたはパスワードが間違っています"
}
```

### GET /api/v1/auth/me
現在のユーザー情報取得

**ヘッダー**
```
Authorization: Bearer {token}
```

**レスポンス (200 OK)**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "ユーザー名",
  "role": "customer"
}
```

---

## 🍱 公開メニューエンドポイント（担当者B）

### GET /api/v1/menus/
メニュー一覧取得

**クエリパラメータ**
- `limit`: 取得件数（デフォルト: 50）
- `offset`: 開始位置（デフォルト: 0）
- `category`: カテゴリフィルタ（オプション）

**レスポンス (200 OK)**
```json
{
  "items": [
    {
      "id": 1,
      "name": "唐揚げ弁当",
      "description": "ジューシーな唐揚げがメインの人気弁当",
      "price": 500,
      "category": "meat",
      "image_url": "https://example.com/images/karaage.jpg",
      "is_available": true,
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00"
    },
    {
      "id": 2,
      "name": "焼肉弁当",
      "description": "特製タレの焼肉がたっぷり",
      "price": 700,
      "category": "meat",
      "image_url": "https://example.com/images/yakiniku.jpg",
      "is_available": true,
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00"
    }
  ],
  "total": 2,
  "limit": 50,
  "offset": 0
}
```

### GET /api/v1/menus/{menu_id}
メニュー詳細取得

**レスポンス (200 OK)**
```json
{
  "id": 1,
  "name": "唐揚げ弁当",
  "description": "ジューシーな唐揚げがメインの人気弁当",
  "price": 500,
  "category": "meat",
  "image_url": "https://example.com/images/karaage.jpg",
  "is_available": true,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

**エラーレスポンス (404 Not Found)**
```json
{
  "detail": "メニューが見つかりません"
}
```

---

## 🛒 注文エンドポイント（担当者C）

### POST /api/v1/orders/
新規注文作成

**ヘッダー**
```
Authorization: Bearer {token}
```

**リクエスト**
```json
{
  "items": [
    {
      "menu_id": 1,
      "quantity": 2
    },
    {
      "menu_id": 2,
      "quantity": 1
    }
  ],
  "delivery_address": "東京都渋谷区...",
  "delivery_time": "2024-01-01T18:00:00",
  "notes": "辛さ控えめでお願いします"
}
```

**レスポンス (201 Created)**
```json
{
  "id": 1,
  "user_id": 1,
  "status": "pending",
  "total_amount": 1700,
  "delivery_address": "東京都渋谷区...",
  "delivery_time": "2024-01-01T18:00:00",
  "notes": "辛さ控えめでお願いします",
  "items": [
    {
      "id": 1,
      "menu_id": 1,
      "menu_name": "唐揚げ弁当",
      "quantity": 2,
      "unit_price": 500,
      "subtotal": 1000
    },
    {
      "id": 2,
      "menu_id": 2,
      "menu_name": "焼肉弁当",
      "quantity": 1,
      "unit_price": 700,
      "subtotal": 700
    }
  ],
  "created_at": "2024-01-01T16:00:00",
  "updated_at": "2024-01-01T16:00:00"
}
```

### GET /api/v1/orders/
現在のユーザーの注文履歴取得

**ヘッダー**
```
Authorization: Bearer {token}
```

**クエリパラメータ**
- `limit`: 取得件数（デフォルト: 20）
- `offset`: 開始位置（デフォルト: 0）
- `status`: ステータスフィルタ（オプション）

**レスポンス (200 OK)**
```json
{
  "items": [
    {
      "id": 1,
      "status": "delivered",
      "total_amount": 1700,
      "delivery_address": "東京都渋谷区...",
      "delivery_time": "2024-01-01T18:00:00",
      "created_at": "2024-01-01T16:00:00",
      "items_count": 3
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

### GET /api/v1/orders/{order_id}
注文詳細取得

**ヘッダー**
```
Authorization: Bearer {token}
```

**レスポンス (200 OK)**
```json
{
  "id": 1,
  "user_id": 1,
  "status": "delivered",
  "total_amount": 1700,
  "delivery_address": "東京都渋谷区...",
  "delivery_time": "2024-01-01T18:00:00",
  "notes": "辛さ控えめでお願いします",
  "items": [
    {
      "id": 1,
      "menu_id": 1,
      "menu_name": "唐揚げ弁当",
      "quantity": 2,
      "unit_price": 500,
      "subtotal": 1000
    },
    {
      "id": 2,
      "menu_id": 2,
      "menu_name": "焼肉弁当",
      "quantity": 1,
      "unit_price": 700,
      "subtotal": 700
    }
  ],
  "created_at": "2024-01-01T16:00:00",
  "updated_at": "2024-01-01T16:00:00"
}
```

---

## 🏪 店舗管理 - メニュー管理エンドポイント（担当者D）

### GET /api/v1/admin/menus/
管理者用メニュー一覧取得

**ヘッダー**
```
Authorization: Bearer {store_token}
```

**クエリパラメータ**
- `limit`: 取得件数（デフォルト: 50）
- `offset`: 開始位置（デフォルト: 0）
- `include_unavailable`: 販売停止商品も含める（デフォルト: false）

**レスポンス (200 OK)**
```json
{
  "items": [
    {
      "id": 1,
      "name": "唐揚げ弁当",
      "description": "ジューシーな唐揚げがメインの人気弁当",
      "price": 500,
      "category": "meat",
      "image_url": "https://example.com/images/karaage.jpg",
      "is_available": true,
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### POST /api/v1/admin/menus/
新規メニュー追加

**ヘッダー**
```
Authorization: Bearer {store_token}
Content-Type: application/json
```

**リクエスト**
```json
{
  "name": "新しい弁当",
  "description": "美味しい弁当の説明",
  "price": 600,
  "category": "vegetable",
  "image_url": "https://example.com/images/new.jpg",
  "is_available": true
}
```

**レスポンス (201 Created)**
```json
{
  "id": 3,
  "name": "新しい弁当",
  "description": "美味しい弁当の説明",
  "price": 600,
  "category": "vegetable",
  "image_url": "https://example.com/images/new.jpg",
  "is_available": true,
  "created_at": "2024-01-01T15:00:00",
  "updated_at": "2024-01-01T15:00:00"
}
```

### PUT /api/v1/admin/menus/{menu_id}
メニュー更新

**ヘッダー**
```
Authorization: Bearer {store_token}
```

**リクエスト**
```json
{
  "name": "更新された弁当名",
  "description": "更新された説明",
  "price": 650,
  "category": "meat",
  "image_url": "https://example.com/images/updated.jpg",
  "is_available": false
}
```

**レスポンス (200 OK)**
```json
{
  "id": 1,
  "name": "更新された弁当名",
  "description": "更新された説明",
  "price": 650,
  "category": "meat",
  "image_url": "https://example.com/images/updated.jpg",
  "is_available": false,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T15:30:00"
}
```

### DELETE /api/v1/admin/menus/{menu_id}
メニュー削除

**ヘッダー**
```
Authorization: Bearer {store_token}
```

**レスポンス (204 No Content)**
```
(レスポンスボディなし)
```

---

## 📋 店舗管理 - 注文管理エンドポイント（担当者E）

### GET /api/v1/admin/orders/
管理者用注文一覧取得

**ヘッダー**
```
Authorization: Bearer {store_token}
```

**クエリパラメータ**
- `limit`: 取得件数（デフォルト: 50）
- `offset`: 開始位置（デフォルト: 0）
- `status`: ステータスフィルタ（pending, preparing, ready, delivered, cancelled）
- `date_from`: 開始日（YYYY-MM-DD）
- `date_to`: 終了日（YYYY-MM-DD）

**レスポンス (200 OK)**
```json
{
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "user_name": "田中太郎",
      "user_email": "tanaka@example.com",
      "status": "pending",
      "total_amount": 1700,
      "delivery_address": "東京都渋谷区...",
      "delivery_time": "2024-01-01T18:00:00",
      "notes": "辛さ控えめでお願いします",
      "items_count": 3,
      "created_at": "2024-01-01T16:00:00",
      "updated_at": "2024-01-01T16:00:00"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### GET /api/v1/admin/orders/{order_id}
管理者用注文詳細取得

**ヘッダー**
```
Authorization: Bearer {store_token}
```

**レスポンス (200 OK)**
```json
{
  "id": 1,
  "user_id": 1,
  "user_name": "田中太郎",
  "user_email": "tanaka@example.com",
  "status": "pending",
  "total_amount": 1700,
  "delivery_address": "東京都渋谷区...",
  "delivery_time": "2024-01-01T18:00:00",
  "notes": "辛さ控えめでお願いします",
  "items": [
    {
      "id": 1,
      "menu_id": 1,
      "menu_name": "唐揚げ弁当",
      "quantity": 2,
      "unit_price": 500,
      "subtotal": 1000
    },
    {
      "id": 2,
      "menu_id": 2,
      "menu_name": "焼肉弁当",
      "quantity": 1,
      "unit_price": 700,
      "subtotal": 700
    }
  ],
  "created_at": "2024-01-01T16:00:00",
  "updated_at": "2024-01-01T16:00:00"
}
```

### PUT /api/v1/admin/orders/{order_id}/status
注文ステータス更新

**ヘッダー**
```
Authorization: Bearer {store_token}
```

**リクエスト**
```json
{
  "status": "preparing"  // pending, preparing, ready, delivered, cancelled
}
```

**レスポンス (200 OK)**
```json
{
  "id": 1,
  "status": "preparing",
  "updated_at": "2024-01-01T16:30:00"
}
```

**エラーレスポンス (400 Bad Request)**
```json
{
  "detail": "無効なステータスです"
}
```

### GET /api/v1/admin/orders/stats
注文統計取得

**ヘッダー**
```
Authorization: Bearer {store_token}
```

**クエリパラメータ**
- `date_from`: 開始日（YYYY-MM-DD）
- `date_to`: 終了日（YYYY-MM-DD）

**レスポンス (200 OK)**
```json
{
  "total_orders": 150,
  "total_revenue": 125000,
  "status_breakdown": {
    "pending": 10,
    "preparing": 5,
    "ready": 3,
    "delivered": 130,
    "cancelled": 2
  },
  "popular_menus": [
    {
      "menu_id": 1,
      "menu_name": "唐揚げ弁当",
      "order_count": 45,
      "revenue": 22500
    },
    {
      "menu_id": 2,
      "menu_name": "焼肉弁当",
      "order_count": 30,
      "revenue": 21000
    }
  ]
}
```

---

## 📊 共通レスポンス

### エラーレスポンス

**400 Bad Request**
```json
{
  "detail": "リクエストが無効です",
  "errors": [
    {
      "field": "email",
      "message": "有効なメールアドレスを入力してください"
    }
  ]
}
```

**401 Unauthorized**
```json
{
  "detail": "認証が必要です"
}
```

**403 Forbidden**
```json
{
  "detail": "この操作を行う権限がありません"
}
```

**404 Not Found**
```json
{
  "detail": "リソースが見つかりません"
}
```

**422 Validation Error**
```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "価格は正の数である必要があります",
      "type": "value_error"
    }
  ]
}
```

**500 Internal Server Error**
```json
{
  "detail": "内部サーバーエラーが発生しました"
}
```

---

## 🔄 ステータス定義

### 注文ステータス (Order Status)
- `pending`: 注文受付済み
- `preparing`: 調理中
- `ready`: 配達準備完了
- `delivered`: 配達完了
- `cancelled`: キャンセル

### ユーザーロール (User Role)
- `customer`: 一般顧客
- `store`: 店舗管理者

### メニューカテゴリ (Menu Category)
- `meat`: 肉類
- `fish`: 魚類
- `vegetable`: 野菜
- `other`: その他

---

## 📝 開発者へのメモ

1. **認証**: 店舗管理者権限が必要なエンドポイントは、JWTトークンのroleフィールドで'store'を確認すること
2. **バリデーション**: 価格は正の整数、数量は1以上、メールアドレス形式の検証を忘れずに
3. **タイムゾーン**: 全ての日時はUTC形式で保存し、レスポンスはISO 8601形式で返すこと
4. **ページネーション**: limitは最大100まで、offsetは0以上であることを確認すること
5. **画像URL**: image_urlは完全なURL形式であることを確認すること

この仕様書に基づいて、フロントエンドとバックエンドが独立してモックやスタブを使って開発を進めることができます。