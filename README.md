# Running locally

```
docker-compose up --build
```

# Migrating

- Change models.py and schemas.py  
- `$ alembic revision -m "create account table"`
- Write upgrades and downgrades to generated migration
- `$ alembic upgrade head`