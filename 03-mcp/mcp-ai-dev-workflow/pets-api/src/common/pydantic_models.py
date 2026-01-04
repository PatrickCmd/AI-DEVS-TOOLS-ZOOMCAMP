"""
Pydantic models for request/response validation.
Based on OpenAPI 3.1.0 specification (openai.yml).
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator


# Enums
class PetStatus(str, Enum):
    """Pet status in the store."""

    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"


class OrderStatus(str, Enum):
    """Order status."""

    PLACED = "placed"
    APPROVED = "approved"
    DELIVERED = "delivered"


# Pet-related models
class CategoryModel(BaseModel):
    """Pet category model."""

    id: int | None = Field(None, description="Category ID")
    name: str = Field(..., description="Category name", max_length=100)

    class Config:
        from_attributes = True


class TagModel(BaseModel):
    """Pet tag model."""

    id: int | None = Field(None, description="Tag ID")
    name: str = Field(..., description="Tag name", max_length=100)

    class Config:
        from_attributes = True


class PetModel(BaseModel):
    """Pet model with full details."""

    id: int | None = Field(None, description="Pet ID", examples=[1])
    category: CategoryModel | None = Field(None, description="Pet category")
    name: str = Field(..., description="Pet name", examples=["doggie"], max_length=200)
    photo_urls: list[str] = Field(
        ..., description="List of photo URLs", alias="photoUrls", min_length=1
    )
    tags: list[TagModel] | None = Field(default_factory=list, description="Pet tags")
    status: PetStatus | None = Field(
        PetStatus.AVAILABLE, description="Pet status in the store"
    )

    @field_validator("photo_urls")
    @classmethod
    def validate_photo_urls(cls, v):
        """Ensure at least one photo URL is provided."""
        if not v or len(v) == 0:
            raise ValueError("At least one photo URL is required")
        return v

    class Config:
        from_attributes = True
        populate_by_name = True


class PetCreateModel(BaseModel):
    """Model for creating a new pet."""

    category: CategoryModel | None = None
    name: str = Field(..., max_length=200)
    photo_urls: list[str] = Field(..., alias="photoUrls", min_length=1)
    tags: list[TagModel] | None = None
    status: PetStatus | None = PetStatus.AVAILABLE

    class Config:
        populate_by_name = True


class PetUpdateModel(BaseModel):
    """Model for updating an existing pet."""

    category: CategoryModel | None = None
    name: str | None = Field(None, max_length=200)
    photo_urls: list[str] | None = Field(None, alias="photoUrls")
    tags: list[TagModel] | None = None
    status: PetStatus | None = None

    class Config:
        populate_by_name = True


# Store-related models
class OrderModel(BaseModel):
    """Store order model."""

    id: int | None = Field(None, description="Order ID")
    pet_id: int = Field(..., description="Pet ID", alias="petId", gt=0)
    quantity: int = Field(default=1, description="Order quantity", ge=1)
    ship_date: datetime | None = Field(None, description="Shipping date", alias="shipDate")
    status: OrderStatus | None = Field(
        OrderStatus.PLACED, description="Order status"
    )
    complete: bool = Field(default=False, description="Order completion status")

    class Config:
        from_attributes = True
        populate_by_name = True


class OrderCreateModel(BaseModel):
    """Model for creating a new order."""

    pet_id: int = Field(..., alias="petId", gt=0)
    quantity: int = Field(default=1, ge=1)
    ship_date: datetime | None = Field(None, alias="shipDate")
    status: OrderStatus | None = OrderStatus.PLACED
    complete: bool = False

    class Config:
        populate_by_name = True


# User-related models
class UserModel(BaseModel):
    """User model."""

    id: int | None = Field(None, description="User ID")
    username: str = Field(..., description="Username", min_length=3, max_length=150)
    first_name: str | None = Field(None, description="First name", alias="firstName", max_length=150)
    last_name: str | None = Field(None, description="Last name", alias="lastName", max_length=150)
    email: EmailStr | None = Field(None, description="Email address")
    password: str = Field(..., description="Password (will be hashed)", min_length=8)
    phone: str | None = Field(None, description="Phone number", max_length=20)
    user_status: int | None = Field(
        0, description="User status code", alias="userStatus", ge=0
    )

    class Config:
        from_attributes = True
        populate_by_name = True


class UserCreateModel(BaseModel):
    """Model for creating a new user."""

    username: str = Field(..., min_length=3, max_length=150)
    first_name: str | None = Field(None, alias="firstName", max_length=150)
    last_name: str | None = Field(None, alias="lastName", max_length=150)
    email: EmailStr | None = None
    password: str = Field(..., min_length=8)
    phone: str | None = Field(None, max_length=20)
    user_status: int | None = Field(0, alias="userStatus", ge=0)

    class Config:
        populate_by_name = True


class UserUpdateModel(BaseModel):
    """Model for updating an existing user."""

    username: str | None = Field(None, min_length=3, max_length=150)
    first_name: str | None = Field(None, alias="firstName", max_length=150)
    last_name: str | None = Field(None, alias="lastName", max_length=150)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8)
    phone: str | None = Field(None, max_length=20)
    user_status: int | None = Field(None, alias="userStatus", ge=0)

    class Config:
        populate_by_name = True


class UserLoginModel(BaseModel):
    """Model for user login."""

    username: str = Field(..., description="Username for login")
    password: str = Field(..., description="Password for login")


# API Response models
class ApiResponseModel(BaseModel):
    """Standard API response model."""

    code: int = Field(..., description="Response code")
    type: str = Field(..., description="Response type")
    message: str = Field(..., description="Response message")

    class Config:
        from_attributes = True
