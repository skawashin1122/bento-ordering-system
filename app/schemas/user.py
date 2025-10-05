"""
ユーザー・認証関連のPydanticスキーマ
API_SPECS.mdの仕様に基づいたデータ構造定義
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.db.models import UserRole


class UserCreate(BaseModel):
    """ユーザー登録用スキーマ"""

    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=8, description="パスワード（8文字以上）")
    name: str = Field(..., min_length=1, max_length=100, description="ユーザー名")
    role: UserRole = Field(default=UserRole.CUSTOMER, description="ユーザーロール")


class UserLogin(BaseModel):
    """ログイン用スキーマ"""

    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., description="パスワード")


class UserResponse(BaseModel):
    """ユーザー情報レスポンス用スキーマ"""

    id: int = Field(..., description="ユーザーID")
    email: EmailStr = Field(..., description="メールアドレス")
    name: str = Field(..., description="ユーザー名")
    role: UserRole = Field(..., description="ユーザーロール")

    model_config = ConfigDict(from_attributes=True)


class UserInDB(BaseModel):
    """データベース内のユーザー情報スキーマ"""

    id: int
    email: EmailStr
    name: str
    hashed_password: str
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """トークンレスポンス用スキーマ"""

    access_token: str = Field(..., description="JWTアクセストークン")
    token_type: str = Field(..., description="トークンタイプ")
    user: UserResponse = Field(..., description="ユーザー情報")


class TokenData(BaseModel):
    """トークンペイロード用スキーマ"""

    email: str | None = Field(None, description="メールアドレス")


class UserRegisterResponse(BaseModel):
    """ユーザー登録レスポンス用スキーマ"""

    message: str = Field(..., description="登録完了メッセージ")
    user: UserResponse = Field(..., description="登録されたユーザー情報")


# 型ヒント用のエイリアス
__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserInDB",
    "Token",
    "TokenData",
    "UserRegisterResponse",
]
