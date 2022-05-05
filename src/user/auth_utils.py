from datetime import timedelta, datetime
from typing import Optional

from core.settings import settings
from jose import jwt


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(
        claims=to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ENCODING_ALGORITHM,
    )
