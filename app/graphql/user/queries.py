import strawberry
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info

from app.auth.jwt import create_jwt, verify_user
from app.graphql.context import GraphQLContext
from app.graphql.permissions import IsAuthenticated
from app.graphql.user.inputs import LoginInput
from app.graphql.user.types import AuthPayload, UserType


@strawberry.type
class UserQuery:

    @strawberry.field(description="Login an existing user")
    async def login(self, info: Info, input_data: LoginInput) -> AuthPayload:
        context: GraphQLContext = info.context
        db: AsyncSession = context.db

        # TODO: move this login logic to a service
        user = await verify_user(db, input_data)
        token = await create_jwt(user)
        return AuthPayload(token=token)

    @strawberry.field(description="Get current user information", permission_classes=[IsAuthenticated])
    async def me(self, info: Info) -> UserType:
        context: GraphQLContext = info.context
        return UserType.from_orm(context.user)
