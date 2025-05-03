import strawberry

from app.graphql.user.mutations import UserMutation
from app.graphql.user.queries import UserQuery


@strawberry.type
class Query(UserQuery):
    pass


@strawberry.type
class Mutation(UserMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
