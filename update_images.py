import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avk_project.settings")
django.setup()

from shop.models import Product  # adjust import if your model name is different
from django.core.files import File

DEFAULT_IMAGE_PATH = os.path.join('static', 'uploads', 'default.png')  # path to default image

for product in Product.objects.all():
    if not product.product_image:
        with open(DEFAULT_IMAGE_PATH, 'rb') as f:
            product.product_image.save('default.png', File(f), save=True)
        print(f"Updated product '{product.name}' with default image.")

print("All missing images have been updated.")
