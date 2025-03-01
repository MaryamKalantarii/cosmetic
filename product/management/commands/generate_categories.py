from django.core.management.base import BaseCommand
from faker import Faker
from product.models import ProductCategoryModel, ColorModel
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Generate fake categories and colors'
    def handle(self, *args, **options):
        fake = Faker()
        # Generate fake categories
        for _ in range(10):
            title = fake.word()
            slug = slugify(title, allow_unicode=True)
            ProductCategoryModel.objects.get_or_create(title=title, slug=slug)
        self.stdout.write(self.style.SUCCESS(
            'Successfully generated 10 fake categories'))
        # Generate fake colors
        for _ in range(10):
            name = fake.color_name()
            hex_code = fake.hex_color()
            ColorModel.objects.get_or_create(name=name, hex_code=hex_code)
        self.stdout.write(self.style.SUCCESS(
            'Successfully generated 10 fake colors'))