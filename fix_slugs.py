# fix_slugs.py

import os
import django
from django.utils.text import slugify

# Tell Django where your settings are
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avk_project.settings')
django.setup()

# Now import your models safely
from shop.models import Catagory, Product

# Fix category slugs
for cat in Catagory.objects.all():
    if not cat.slug:
        cat.slug = slugify(cat.name)
        cat.save()
        print(f"✅ Fixed category slug: {cat.name} → {cat.slug}")

# Fix product slugs
for prod in Product.objects.all():
    if not prod.slug:
        prod.slug = slugify(prod.name)
        prod.save()
        print(f"✅ Fixed product slug: {prod.name} → {prod.slug}")

print("🎉 Slugs fixed successfully!")
