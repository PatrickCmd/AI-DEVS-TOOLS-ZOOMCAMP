"""
GraphQL URL configuration for the TODO application.

This module defines the GraphQL endpoint with GraphiQL documentation interface.
"""

from django.urls import path
from strawberry.django.views import GraphQLView
from .schema import schema


urlpatterns = [
    path("", GraphQLView.as_view(schema=schema, graphiql=True), name="graphql"),
]
