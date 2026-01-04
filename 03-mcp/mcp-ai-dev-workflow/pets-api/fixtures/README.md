# Fixtures Directory

This directory contains Django fixtures for the Petstore API. Fixtures are used to load pre-defined data into the database, which is useful for testing, development, and sharing consistent data with contributors.

## Available Fixtures

### Sample Fixtures (Pre-created)

- **sample_categories_tags.json**: Contains 5 categories (Dogs, Cats, Birds, Fish, Reptiles) and 8 tags (friendly, playful, calm, trained, energetic, gentle, social, independent)

### Custom Fixtures (Created by dump commands)

- **pets_categories_tags.json**: Categories and Tags exported from your database
- **pets_pets.json**: Pet records exported from your database
- **users.json**: User records exported from your database
- **store_orders.json**: Order records exported from your database

## Usage

### Loading Fixtures

```bash
# Load all fixtures
make load-fixtures

# Load sample data (categories and tags)
make create-sample
```

### Creating Fixtures from Database

```bash
# Export all data to fixtures
make dump-fixtures

# Export specific app data
make dump-pets
make dump-users
make dump-store
```

### Manual Loading (Using Django Commands)

```bash
# Load a specific fixture
docker compose exec backend python src/manage.py loaddata fixtures/sample_categories_tags.json

# Load multiple fixtures
docker compose exec backend python src/manage.py loaddata fixtures/users.json fixtures/pets_categories_tags.json
```

### Manual Creation (Using Django Commands)

```bash
# Dump specific models
docker compose exec backend python src/manage.py dumpdata pets.Category pets.Tag --indent 2 --output fixtures/my_fixture.json

# Dump entire app
docker compose exec backend python src/manage.py dumpdata pets --indent 2 --output fixtures/pets_all.json

# Dump all data (excluding contenttypes and sessions)
docker compose exec backend python src/manage.py dumpdata --exclude contenttypes --exclude sessions --indent 2 --output fixtures/full_backup.json
```

## Use Cases

### 1. Testing
Load fixtures before running tests to ensure consistent test data:
```bash
make create-sample
make test
```

### 2. Development
Start with pre-populated data for easier development:
```bash
make setup
make create-sample
```

### 3. Sharing Data with Contributors
Export your current database state and share with team:
```bash
make dump-fixtures
# Commit fixtures/ directory to git
# Contributors can then run: make load-fixtures
```

### 4. Backup and Restore
Create periodic backups of important data:
```bash
# Backup
make dump-fixtures

# Restore (after reset-db)
make reset-db
make load-fixtures
```

## Best Practices

1. **Version Control**: Commit sample fixtures to git, but be careful with user data
2. **Sensitive Data**: Never commit fixtures containing real user passwords or sensitive information
3. **Primary Keys**: Be aware that fixtures include primary keys, which may conflict with existing data
4. **Load Order**: Load fixtures in dependency order (users → categories/tags → pets → orders)
5. **Testing**: Keep test fixtures separate from production data exports

## Notes

- Fixtures are in JSON format by default
- The `--indent 2` flag makes fixtures human-readable
- Use `--natural-foreign-keys` and `--natural-primary-keys` for more portable fixtures
- Fixtures can include data from multiple models in a single file
