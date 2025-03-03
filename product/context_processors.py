from product.models import ProductCategoryModel

def categories_processor(request):
    category = ProductCategoryModel.objects.all()

    return{
        'categories': category
    }