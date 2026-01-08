# Pets Store App 🐾🛒

A clean, modern **Django 5** demo project for a small **pet store** experience:
- Browse **pets** available for adoption 🐶🐱🐰
- Browse **products** like food, toys, accessories 🧸🍖🎁
- Beautiful UI using **TailwindCSS** + **Font Awesome**
- Admin area branded as **Pets Store Admin**

---

## Screens & Routes

| Route | What it is |
|---|---|
| `/` | Home page (stats + featured pets/products) |
| `/catalog/` | Catalog page (search + filters) |
| `/pets/<id>/` | Pet detail page |
| `/products/<id>/` | Product detail page |
| `/admin/` | Admin dashboard (Pets Store Admin) |

---

## Tech Stack

- Python 3.12+
- Django 5.2.4
- SQLite (default)
- TailwindCSS (via CDN for fast iteration)
- Font Awesome (via CDN)
- `uv` for dependency management

---

## Quickstart (with `uv` + Make)

### 1) Install dependencies

```bash
make install
```

### 2) Run migrations

```bash
make migrate
```

### 3) (Optional) Seed sample data 🐾

Create synthetic pets/products so the UI looks great immediately:

```bash
make seed
```

With custom counts + reproducible randomness:

```bash
make seed PETS=30 PRODUCTS=40 SEED=7
```

Reset and re-seed:

```bash
make seed-clear SEED=42
```

### 4) Create an admin user

#### Option A: One-command dev admin (non-interactive)
Creates/updates:
- username: `admin`
- email: `admin@example.com`
- password: `admin123`

```bash
make createsuperuser-admin
```

#### Option B: Standard Django (interactive)

```bash
make createsuperuser ARGS="--username admin --email admin@example.com"
```

### 5) Run the server

```bash
make run
```

Open:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## Management Commands

### `seed_store`

Seeds the database with synthetic pets and products.

Examples:

```bash
uv run python manage.py seed_store
uv run python manage.py seed_store --clear
uv run python manage.py seed_store --pets 25 --products 30 --seed 123
```

Arguments:
- `--pets`: number of pets to generate (default: 18)
- `--products`: number of products to generate (default: 24)
- `--clear`: delete existing `Pet` and `Product` rows first
- `--seed`: integer seed for reproducible results

---

## Data Model Overview

### `Pet`
- `name`, `pet_type`, `breed`, `age_years`
- `price` (decimal)
- `in_stock` (availability)
- `emoji` (for friendly UI)
- `description`

### `Product`
- `name`, `category`
- `price` (decimal)
- `in_stock`
- `icon` (Font Awesome class, e.g. `fa-bone`)
- `description`

---

## Development Notes

- This is a template/demo app (e.g. "Adopt" / "Add to cart" buttons are UI-only).
- Keep complex logic in **views** (not templates) where possible.
- Tailwind is loaded via CDN for simplicity; for production you would typically compile Tailwind.

---

## Common Commands

```bash
make test
make clean
python manage.py check
```

---

## License

Use freely for learning, demos, and prototypes.
