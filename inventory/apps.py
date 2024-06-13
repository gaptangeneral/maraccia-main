# inventory/apps.py
from django.apps import AppConfig


class InventoryConfig(AppConfig):  # Sınıf adı doğru yazıldı
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'