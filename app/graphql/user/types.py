import uuid
from datetime import datetime
from typing import Optional

import strawberry

from app.models import User


@strawberry.type
class UserType:
    id: uuid.UUID
    email: str
    username: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]

    @classmethod
    def from_orm(cls, user: User) -> "UserType":
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            avatar_url=user.avatar_url,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


@strawberry.type
class AuthPayload:
    token: str
    token_type: str = "Bearer"
