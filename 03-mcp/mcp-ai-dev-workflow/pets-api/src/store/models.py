"""
Store models for the Petstore API.
"""

from django.conf import settings
from django.db import models


class Order(models.Model):
    """
    Store order model representing a purchase order for a pet.
    Based on the OpenAPI specification.
    """

    class Status(models.TextChoices):
        PLACED = "placed", "Placed"
        APPROVED = "approved", "Approved"
        DELIVERED = "delivered", "Delivered"

    pet = models.ForeignKey(
        "pets.Pet",
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="Pet being ordered"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
        help_text="User who placed the order"
    )

    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Quantity of pets ordered"
    )

    ship_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Expected shipping date"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLACED,
        help_text="Order status"
    )

    complete = models.BooleanField(
        default=False,
        help_text="Whether the order is complete"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["complete"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.pet.name} ({self.get_status_display()})"

    def __repr__(self):
        return f"<Order id={self.id}, pet={self.pet_id}, status={self.status}>"
