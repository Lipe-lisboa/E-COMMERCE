from pathlib import Path

from django.conf import settings
from PIL import Image

def resize_image(image_django, new_width=800, optimize=True, quality=60):
    image_path = Path(settings.MEDIA_ROOT / image_django.name).resolve()
    img = Image.open(image_path)
    original_width, original_height = img.size

    if original_width <= new_width:
        img.close()
        return img

    
    #regra de 3
    new_height = round(new_width * original_height / original_width)

    new_image = img.resize((new_width, new_height), Image.LANCZOS)

    new_image.save(
        image_path,
        optimize=optimize,
        quality=quality,
    )

    return new_image