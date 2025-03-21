import os

folders = [
    "app/api/v1/routes",
    "app/core",
    "app/models",
    "app/schemas",
    "app/services",
    "migrations",
]

files = [
    ".env",
    "requirements.txt",
    "README.md",
    "app/__init__.py",
    "app/main.py",
    "app/api/v1/__init__.py",
    "app/api/v1/routes/__init__.py",
    "app/api/v1/routes/items.py",
    "app/api/v1/routes/users.py",
    "app/api/v1/routes/auth.py",
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/database.py",
    "app/core/security.py",
    "app/models/__init__.py",
    "app/models/item.py",
    "app/models/user.py",
    "app/schemas/__init__.py",
    "app/schemas/item.py",
    "app/schemas/user.py",
    "app/services/__init__.py",
    "app/services/item_service.py",
    "app/services/user_service.py",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    open(file, "a").close()  # Create an empty file
