from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Pet, Product


def home(request):
    featured_pets = Pet.objects.filter(in_stock=True)[:6]
    featured_products = Product.objects.filter(in_stock=True)[:6]

    context = {
        "featured_pets": featured_pets,
        "featured_products": featured_products,
        "stats": {
            "pets": Pet.objects.count(),
            "products": Product.objects.count(),
            "in_stock_pets": Pet.objects.filter(in_stock=True).count(),
            "in_stock_products": Product.objects.filter(in_stock=True).count(),
        },
    }
    return render(request, "home.html", context)


def catalog(request):
    q = (request.GET.get("q") or "").strip()
    pet_type = (request.GET.get("pet_type") or "").strip()
    category = (request.GET.get("category") or "").strip()

    pets = Pet.objects.all()
    products = Product.objects.all()

    if q:
        pets = pets.filter(Q(name__icontains=q) | Q(breed__icontains=q) | Q(description__icontains=q))
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    if pet_type:
        pets = pets.filter(pet_type=pet_type)

    if category:
        products = products.filter(category=category)

    context = {
        "q": q,
        "pet_type": pet_type,
        "category": category,
        "pets": pets,
        "products": products,
        "pet_types": Pet.PetType.choices,
        "categories": Product.Category.choices,
        "counts": {
            "pets": pets.count(),
            "products": products.count(),
        },
    }
    return render(request, "catalog.html", context)


def pet_detail(request, pk: int):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, "pet_detail.html", {"pet": pet})


def product_detail(request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})
