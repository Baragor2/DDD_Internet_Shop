from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Container

import bcrypt
from passlib.context import CryptContext
import jwt

from settings.config import Config


@dataclass
class Auth:
    config: Config
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def validate_password(self, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password)

    async def get_password_hash(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=30)
        to_encode.update({"exp": expire})

        secret_key = self.config.auth.private_key_pass.read_text().encode()
        encoded_jwt = jwt.encode(
            to_encode, secret_key, algorithm=self.config.auth.algorithm
        )
        return encoded_jwt
