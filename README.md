[![Docker Image CI](https://github.com/tncoding/platfrom-backend/actions/workflows/main.yml/badge.svg)](https://github.com/tncoding/platfrom-backend/actions/workflows/main.yml)
# Running locally

```
docker-compose up --build
```

# Migrating

- Change models.py and schemas.py  
- `$ alembic revision -m "create account table"`
- Write upgrades and downgrades to generated migration
- `$ alembic upgrade head`
