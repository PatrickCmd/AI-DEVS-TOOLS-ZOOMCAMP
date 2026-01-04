"""
Pet models for the Petstore API.
"""

from django.db import models


class Category(models.Model):
    """Pet category model."""

    name = models.CharField(max_length=100, unique=True, help_text="Category name")

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Category {self.name} (id={self.id})>"


class Tag(models.Model):
    """Pet tag model."""

    name = models.CharField(max_length=100, unique=True, help_text="Tag name")

    class Meta:
        db_table = "tags"
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Tag {self.name} (id={self.id})>"


class Pet(models.Model):
    """
    Pet model representing a pet in the store.
    Based on the OpenAPI specification.
    """

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        PENDING = "pending", "Pending"
        SOLD = "sold", "Sold"

    name = models.CharField(max_length=200, help_text="Pet name")

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pets",
        help_text="Pet category"
    )

    photo_urls = models.JSONField(
        default=list,
        help_text="List of photo URLs for the pet"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="pets",
        help_text="Pet tags"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
        help_text="Pet availability status in the store"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pets"
        verbose_name = "Pet"
        verbose_name_plural = "Pets"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def __repr__(self):
        return f"<Pet {self.name} (id={self.id}, status={self.status})>"
