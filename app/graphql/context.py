from typing import Optional

from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext

from app.database import get_db
from app.models import User


class GraphQLContext(BaseContext):
    def __init__(self, request: Request, response: Response, db: AsyncSession, user: Optional[User] = None):
        super().__init__()
        self.request = request
        self.response = response
        self.db = db
        self.user = user


async def get_context(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> GraphQLContext:
    return GraphQLContext(
        request=request,
        response=response,
        db=db,
        user=None,  # Initialize as None, will be set by permission classes
    )
