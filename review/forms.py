from django import forms
from .models import ReviewModel
from product.models import ProductModel,ProductStatusType

class SubmitReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ['product','rating', 'description']
        error_messages = {
            'description': {
                'required': 'فیلد توضیحات اجباری است',
            },
        }
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        rating = cleaned_data.get('rating')

        # بررسی مقدار امتیاز (باید بین ۱ تا ۵ باشد)
        if rating not in [1, 2, 3, 4, 5]:
            raise forms.ValidationError("امتیاز معتبر نیست. مقدار امتیاز باید بین ۱ تا ۵ باشد.")

        # بررسی وضعیت محصول
        try:
            ProductModel.objects.get(id=product.id, status=ProductStatusType.publish.value)
        except ProductModel.DoesNotExist:
            raise forms.ValidationError("این محصول وجود ندارد یا منتشر نشده است.")

        return cleaned_data