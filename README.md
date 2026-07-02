### Celery Command: 
```celery -A paliwalsamaj worker --loglevel=info```

### Redis Start Command: 
```brew services start redis```

### Test if redis is working: 
```redis-cli ping```

### Re-Create Local File
```django-admin makemessages -l hi```

### Compile Local File
```python manage.py compilemessages```

### Data Migration Script
```python manage.py makemigrations --empty SamajApp```

### Run with Docker
1. (Optional) Update values in `.env` for your environment.
2. Start all services:
   ```bash
   docker compose up --build
   ```
3. Open the app at `http://localhost:8000`.

### Docker Services
- `web`: Django app (`runserver`) on port `8000`
- `worker`: Celery worker
- `db`: PostgreSQL on port `5432`
- `redis`: Redis on port `6379`