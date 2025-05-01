from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.admin import admin
from app.config import settings
from app.graphql.context import get_context
from app.graphql.schema import schema

app = FastAPI(title=settings.app_name, version=settings.app_version)

graphql_app = GraphQLRouter(schema, context_getter=get_context, graphql_ide=settings.graphql_sandbox)
app.include_router(graphql_app, prefix="/graphql")
admin.mount_to(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
