"""
アプリケーション設定
Pydantic Settingsを使用した型安全な設定管理
"""

import os
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定クラス"""
    
    # アプリケーション基本情報
    app_name: str = Field(default="弁当注文管理システム", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    
    # データベース設定
    database_url: str = Field(
        default="postgresql+asyncpg://bento_user:bento_password@localhost:5432/bento_ordering",
        alias="DATABASE_URL"
    )
    
    # セキュリティ設定
    secret_key: str = Field(
        default="your-secret-key-change-this-in-production",
        alias="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, 
        alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    
    # CORS設定
    allowed_origins: List[str] = Field(
        default=["http://localhost:8000", "http://127.0.0.1:8000"],
        alias="ALLOWED_ORIGINS"
    )
    
    # ページネーション設定
    default_page_size: int = Field(default=20)
    max_page_size: int = Field(default=100)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# グローバル設定インスタンス
settings = Settings()


def get_settings() -> Settings:
    """設定インスタンスを取得（依存性注入用）"""
    return settings