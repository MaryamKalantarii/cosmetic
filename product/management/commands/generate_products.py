from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal
from django.utils.text import slugify
from product.models import ProductModel, ProductCategoryModel, ColorModel,ProductColorStock
from pathlib import Path
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent

class Command(BaseCommand):
    help = 'Generate fake products with color stock'

    def handle(self, *args, **options):
        fake = Faker()

        # لیست تصاویر موجود در پوشه images
        image_list = [f"images/img{i}.png" for i in range(1, 22)]

        categories = list(ProductCategoryModel.objects.all())
        colors = list(ColorModel.objects.all())

        if not categories:
            self.stdout.write(self.style.WARNING('❌ No categories found. Run category seeder first.'))
            return

        if not colors:
            self.stdout.write(self.style.WARNING('❌ No colors found. Run color seeder first.'))
            return

        for _ in range(10):  # ایجاد 10 محصول
            title = fake.sentence(nb_words=3)
            slug = slugify(title, allow_unicode=True)
            description = fake.paragraph()
            avg_rate = round(random.uniform(0, 5), 1)
            status = 1  # منتشر شده
            price = Decimal(random.randint(1000, 50000))
            discount_percent = random.randint(0, 50)
            views = random.randint(0, 1000)

            # انتخاب تصویر تصادفی
            selected_image = random.choice(image_list)
            image_path = BASE_DIR / selected_image
            image_obj = File(open(image_path, "rb"), name=Path(selected_image).name)

            # ایجاد محصول
            product = ProductModel.objects.create(
                title=title,
                slug=slug,
                description=description,
                avg_rate=avg_rate,
                status=status,
                price=price,
                discount_percent=discount_percent,
                views=views,
                image1=image_obj,
            )

            # اضافه کردن دسته‌بندی تصادفی به محصول
            product.category.set(random.sample(categories, k=random.randint(1, len(categories))))

            # اضافه کردن رنگ‌های تصادفی و موجودی آنها
            total_stock = 0
            selected_colors = random.sample(colors, k=random.randint(1, 5))  # هر محصول 1 تا 5 رنگ دارد
            for color in selected_colors:
                stock = random.randint(1, 20)  # مقدار تصادفی برای موجودی هر رنگ
                ProductColorStock.objects.create(product=product, color=color, stock=stock)
                total_stock += stock

            # به‌روزرسانی موجودی کلی محصول بر اساس مجموع رنگ‌ها
            product.stock = total_stock
            product.save(update_fields=['stock'])

        self.stdout.write(self.style.SUCCESS('✅ Successfully generated 10 fake products with colors and stock'))