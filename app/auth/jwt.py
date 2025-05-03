import base64
from datetime import UTC, datetime, timedelta

import jwt
from argon2.exceptions import VerifyMismatchError
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.graphql.user.inputs import LoginInput
from app.models.user import User
from app.services.user import UserService
from app.utils import ph

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
AES_KEY = bytes.fromhex(settings.aes_key)
AES_IV = bytes.fromhex(settings.aes_iv)


async def create_jwt(user: User) -> str:
    payload = {
        "user_id": str(user.id),
        "exp": datetime.now(UTC) + timedelta(minutes=settings.token_expire_minutes),
    }
    print(f"BLYAT {payload['exp']=}")
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
    encryptor = cipher.encryptor()

    pad_len = 16 - (len(token) % 16)
    padded_token = token + (" " * pad_len)
    encrypted_token = encryptor.update(padded_token.encode()) + encryptor.finalize()

    return base64.urlsafe_b64encode(encrypted_token).decode()


async def decrypt_jwt(db: AsyncSession, token: str = Depends(oauth2_scheme)) -> User:
    user_service = UserService(db)
    try:
        encrypted_token = base64.urlsafe_b64decode(token)

        cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_token = decryptor.update(encrypted_token) + decryptor.finalize()

        token = decrypted_token.decode().rstrip()
        decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return await user_service.get_user("id", decoded["user_id"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")


async def verify_user(db: AsyncSession, user_data: LoginInput) -> User:
    user_service = UserService(db)
    try:
        user = await user_service.get_user("email", user_data.email)
        ph.verify(user.password_hash, user_data.password)
    except VerifyMismatchError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user credentials!")

    return user
