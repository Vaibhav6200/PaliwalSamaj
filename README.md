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