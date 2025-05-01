from typing import Any

from fastapi import HTTPException, status
from strawberry.permission import BasePermission
from strawberry.types import Info

from app.auth.jwt import decrypt_jwt


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request = info.context.request
        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=self.message)

        try:
            user = await decrypt_jwt(info.context.db, token)
            info.context.user = user
            return True
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")


class IsSuperuser(BasePermission):
    message = "User must be a superuser"

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        if not hasattr(info.context, "user") or not info.context["user"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

        if not info.context["user"].is_superuser:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=self.message)

        return True
