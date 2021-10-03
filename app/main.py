# import sys
# sys.path.append(r"/home/gleb/tabs/web/venv/lib/python3.8/site-packages")

from fastapi import FastAPI
from graphene import ObjectType, String, Schema
from starlette.graphql import GraphQLApp


# from .routers import end_points


class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name


app = FastAPI()

app.add_route("/", GraphQLApp(schema=Schema(query=Query)))

# app.include_router(end_points.router)
