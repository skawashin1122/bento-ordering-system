"""
セキュリティ関連の機能
パスワードハッシュ化、JWT認証など
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# パスワードハッシュ化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    平文パスワードとハッシュ化パスワードを比較
    
    Args:
        plain_password: 平文パスワード
        hashed_password: ハッシュ化パスワード
    
    Returns:
        bool: 一致する場合True
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    パスワードをハッシュ化
    
    Args:
        password: 平文パスワード
    
    Returns:
        str: ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    JWTアクセストークンを生成
    
    Args:
        data: トークンに含めるデータ
        expires_delta: 有効期限（指定しない場合はデフォルト値を使用）
    
    Returns:
        str: JWTトークン
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    JWTトークンを検証してペイロードを取得
    
    Args:
        token: JWTトークン
    
    Returns:
        Optional[Dict[str, Any]]: ペイロード、無効な場合はNone
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None