"""
GraphQL schema for the TODO application.

This module defines the complete GraphQL schema combining queries and mutations.
"""

import strawberry
from .queries import Query
from .mutations import Mutation


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    # Enable GraphiQL documentation interface
    subscription=None
)
