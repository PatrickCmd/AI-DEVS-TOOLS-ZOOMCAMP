from django.db import models
from django.urls import reverse


class Pet(models.Model):
    class PetType(models.TextChoices):
        DOG = "dog", "Dog"
        CAT = "cat", "Cat"
        BIRD = "bird", "Bird"
        FISH = "fish", "Fish"
        RABBIT = "rabbit", "Rabbit"
        REPTILE = "reptile", "Reptile"
        OTHER = "other", "Other"

    name = models.CharField(max_length=80)
    pet_type = models.CharField(max_length=20, choices=PetType.choices)
    breed = models.CharField(max_length=80, blank=True)
    age_years = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    emoji = models.CharField(max_length=4, default="🐾")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_pet_type_display()})"

    def get_absolute_url(self):
        return reverse("pet_detail", args=[self.pk])


class Product(models.Model):
    class Category(models.TextChoices):
        FOOD = "food", "Food"
        TOY = "toy", "Toy"
        GROOMING = "grooming", "Grooming"
        ACCESSORY = "accessory", "Accessory"
        HEALTH = "health", "Health"
        OTHER = "other", "Other"

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=Category.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    icon = models.CharField(max_length=40, default="fa-box")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.pk])
