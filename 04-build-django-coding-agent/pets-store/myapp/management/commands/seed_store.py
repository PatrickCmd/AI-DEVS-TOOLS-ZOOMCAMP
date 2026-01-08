from __future__ import annotations

import random
from decimal import Decimal

from django.core.management.base import BaseCommand

from myapp.models import Pet, Product


class Command(BaseCommand):
    help = "Seed the database with synthetic pets and products for Pets Store App. 🐾"

    def add_arguments(self, parser):
        parser.add_argument("--pets", type=int, default=18, help="Number of pets to create (default: 18)")
        parser.add_argument(
            "--products", type=int, default=24, help="Number of products to create (default: 24)"
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing Pet and Product rows before seeding",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="Random seed for reproducible data",
        )

    def handle(self, *args, **options):
        pets_n: int = options["pets"]
        products_n: int = options["products"]
        clear: bool = options["clear"]
        seed = options["seed"]

        if seed is not None:
            random.seed(seed)

        if clear:
            Pet.objects.all().delete()
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing pets and products."))

        created_pets = self._seed_pets(pets_n)
        created_products = self._seed_products(products_n)

        self.stdout.write(self.style.SUCCESS(f"Seed complete ✅  Pets: +{created_pets}  Products: +{created_products}"))

    def _seed_pets(self, n: int) -> int:
        names_by_type = {
            Pet.PetType.DOG: ["Buddy", "Luna", "Max", "Daisy", "Rocky", "Milo", "Bella"],
            Pet.PetType.CAT: ["Whiskers", "Cleo", "Oliver", "Nala", "Simba", "Mochi", "Pepper"],
            Pet.PetType.BIRD: ["Kiwi", "Sunny", "Rio", "Pico", "Skye"],
            Pet.PetType.FISH: ["Bubbles", "Neon", "Coral", "Finley"],
            Pet.PetType.RABBIT: ["Clover", "Snowball", "Hazel", "Thumper"],
            Pet.PetType.REPTILE: ["Spike", "Ziggy", "Saffron", "Nova"],
            Pet.PetType.OTHER: ["Peanut", "Waffles", "Bean"],
        }

        emoji_by_type = {
            Pet.PetType.DOG: "🐶",
            Pet.PetType.CAT: "🐱",
            Pet.PetType.BIRD: "🐦",
            Pet.PetType.FISH: "🐠",
            Pet.PetType.RABBIT: "🐰",
            Pet.PetType.REPTILE: "🦎",
            Pet.PetType.OTHER: "🐾",
        }

        breeds_by_type = {
            Pet.PetType.DOG: ["Golden Retriever", "Beagle", "Shiba Inu", "Poodle", "Corgi"],
            Pet.PetType.CAT: ["Siamese", "Maine Coon", "British Shorthair", "Tabby"],
            Pet.PetType.BIRD: ["Parakeet", "Cockatiel", "Canary"],
            Pet.PetType.FISH: ["Guppy", "Betta", "Tetra"],
            Pet.PetType.RABBIT: ["Dutch", "Lionhead", "Mini Lop"],
            Pet.PetType.REPTILE: ["Leopard Gecko", "Corn Snake", "Bearded Dragon"],
            Pet.PetType.OTHER: ["Friendly", "Curious"],
        }

        vibe_lines = [
            "Loves treats and belly rubs. 🦴",
            "Gentle, curious, and super cuddly. 💛",
            "Playful energy with a calm heart. ✨",
            "Perfect for first-time pet parents. 🏡",
            "Smart, social, and very photogenic. 📸",
            "A cozy companion for chill evenings. 🛋️",
        ]

        pet_types = [t for t, _ in Pet.PetType.choices]

        to_create: list[Pet] = []
        for _ in range(n):
            pet_type = random.choice(pet_types)
            name = random.choice(names_by_type[pet_type])
            breed = random.choice(breeds_by_type[pet_type])
            age = random.randint(0, 12)
            price = Decimal(random.choice([99, 149, 199, 249, 299, 349, 399, 499]))
            in_stock = random.random() > 0.12
            emoji = emoji_by_type.get(pet_type, "🐾")
            description = random.choice(vibe_lines)

            # reduce duplicates a bit
            if Pet.objects.filter(name=name, pet_type=pet_type, breed=breed).exists():
                name = f"{name} {random.choice(['Jr.', 'II', 'III', '✨', '🐾'])}".strip()

            to_create.append(
                Pet(
                    name=name,
                    pet_type=pet_type,
                    breed=breed,
                    age_years=age,
                    price=price,
                    in_stock=in_stock,
                    emoji=emoji,
                    description=description,
                )
            )

        Pet.objects.bulk_create(to_create)
        return len(to_create)

    def _seed_products(self, n: int) -> int:
        products_by_category = {
            Product.Category.FOOD: [
                ("Crunchy Kibble", "fa-drumstick-bite"),
                ("Salmon Bites", "fa-fish"),
                ("Healthy Treat Mix", "fa-bone"),
                ("Wet Food Variety Pack", "fa-utensils"),
            ],
            Product.Category.TOY: [
                ("Squeaky Ball", "fa-basketball-ball"),
                ("Feather Wand", "fa-feather-alt"),
                ("Chew Rope", "fa-link"),
                ("Puzzle Toy", "fa-puzzle-piece"),
            ],
            Product.Category.GROOMING: [
                ("Soft Brush", "fa-brush"),
                ("Gentle Shampoo", "fa-soap"),
                ("Nail Clippers", "fa-cut"),
            ],
            Product.Category.ACCESSORY: [
                ("Cozy Bed", "fa-bed"),
                ("Adjustable Leash", "fa-grip-lines"),
                ("Travel Carrier", "fa-suitcase-rolling"),
                ("Food Bowl", "fa-bowl-rice"),
            ],
            Product.Category.HEALTH: [
                ("Vitamin Chews", "fa-capsules"),
                ("Flea & Tick Spray", "fa-shield-virus"),
                ("Dental Kit", "fa-tooth"),
            ],
            Product.Category.OTHER: [
                ("Training Clicker", "fa-mouse"),
                ("Pet Wipes", "fa-water"),
            ],
        }

        descriptions = [
            "Top-rated by happy pet parents. ⭐",
            "Durable, safe, and easy to use. ✅",
            "A daily essential for wagging tails. 🐕",
            "Designed for comfort and fun. 🎉",
            "Gentle on sensitive pets. 🌿",
            "A smart upgrade for your routine. ⚡",
        ]

        categories = [c for c, _ in Product.Category.choices]

        to_create: list[Product] = []
        for _ in range(n):
            category = random.choice(categories)
            name, icon = random.choice(products_by_category[category])

            # add variety to product names
            suffix = random.choice(["", " (XL)", " (Mini)", " • Pro", " • Plus", " • Eco"])
            final_name = f"{name}{suffix}".strip()

            price = Decimal(random.choice([5, 8, 9, 12, 14, 19, 24, 29, 39, 49, 79]))
            in_stock = random.random() > 0.10
            description = random.choice(descriptions)

            if Product.objects.filter(name=final_name, category=category).exists():
                final_name = f"{final_name} #{random.randint(2, 99)}"

            to_create.append(
                Product(
                    name=final_name,
                    category=category,
                    price=price,
                    in_stock=in_stock,
                    icon=icon,
                    description=description,
                )
            )

        Product.objects.bulk_create(to_create)
        return len(to_create)
