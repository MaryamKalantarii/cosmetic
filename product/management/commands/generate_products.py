from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal
from django.utils.text import slugify
from product.models import ProductModel, ProductCategoryModel, ColorModel, ProductStatusType
from pathlib import Path
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent

class Command(BaseCommand):

    help = 'Generate fake products'

    def handle(self, *args, **options):
        fake = Faker()
        # List of images
        image_list = [
            "./images/img1.png",
            "./images/img2.png",
            "./images/img3.png",
            "./images/img4.png",
            "./images/img5.png",
            "./images/img6.png",
            "./images/img7.png",
            "./images/img8.png",
            "./images/img9.png",
            "./images/img10.png",
            "./images/img11.png",
            "./images/img12.png",
            "./images/img13.png",
            "./images/img14.png",
            "./images/img15.png",
            "./images/img16.png",
            "./images/img17.png",
            "./images/img18.png",
            "./images/img19.png",
            "./images/img20.png",
            "./images/img21.png",
            
            # Add more image filenames as needed
        ]
        categories = list(ProductCategoryModel.objects.all())
        colors = list(ColorModel.objects.all())

        if not categories:
            self.stdout.write(self.style.WARNING('No categories found. Run category seeder first.'))
            return

        for _ in range(10):
            title = fake.sentence(nb_words=3)
            slug = slugify(title,allow_unicode=True)
            description = fake.paragraph()
            avg_rate = round(random.uniform(0, 5), 1)
            stock = random.randint(0, 100)
            status = ProductStatusType.publish
            price = Decimal(random.randint(1000, 50000))
            discount_percent = random.randint(0, 50)
            views = random.randint(0, 1000)
            
            selected_image = random.choice(image_list)
            image_obj = File(file=open(BASE_DIR / selected_image,"rb"),name=Path(selected_image).name)

            product = ProductModel.objects.create(
                title=title,
                slug=slug,
                description=description,
                avg_rate=avg_rate,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent,
                views=views,
                image1=image_obj,

            )

            
            product.category.set(random.sample(categories, k=random.randint(1, len(categories))))
            product.colors.set(random.sample(colors, k=random.randint(0, len(colors))))


        self.stdout.write(self.style.SUCCESS('Successfully generated 10 fake products'))