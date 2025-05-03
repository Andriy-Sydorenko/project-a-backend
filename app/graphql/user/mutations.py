import strawberry
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info

from app.auth.jwt import create_jwt
from app.graphql.context import GraphQLContext
from app.graphql.user.inputs import RegisterInput
from app.graphql.user.types import AuthPayload
from app.services.user import UserService


@strawberry.type
class UserMutation:

    @strawberry.mutation(description="Register a new user")
    async def register(self, info: Info, input_data: RegisterInput) -> AuthPayload:
        # TODO: find a way to avoid initializing the db session and user service in every resolver
        context: GraphQLContext = info.context
        db: AsyncSession = context.db
        user_service = UserService(db)

        user = await user_service.create_user(
            email=input_data.email,
            password=input_data.password,
            username=input_data.username,
        )

        token = create_jwt(user)
        return AuthPayload(token=token)
