import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rojgarapp.settings")
django.setup()

from app.models import Professions

professions = [
    "Labor",
    "Driver",
    "Jyami",
    "Mistri",
    "Electrician",
    "Plumber",
    "Painter",
    "Mason",
    "Mechanic",
    "Welder",
    "Carpenter",
    "Tailor",
    "Agricultural Worker",
    "Construction Worker",
    "Porter",
    "Cleaner",
    "Waiter",
    "Cook",
    "Security Guard",
    "Delivery Person",
    "Shop Assistant",
    "Street Vendor",
    "Butcher",
    "Fisherman",
    "Rickshaw Driver",
    "Barber",
    "Fruit Seller",
    "Taxi Driver",
    "Auto Rickshaw Driver",
    "Garbage Collector",
]

for name in professions:
    obj, created = Professions.objects.get_or_create(name=name)
    if created:
        print(f"Added: {name}")
    else:
        print(f"Already exists: {name}")
