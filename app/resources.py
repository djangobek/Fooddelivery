from import_export.resources import ModelResource
from .models import Category,Product,BotUserModel
class CategoryResource(ModelResource):
    class Meta:
        model = Category
class ProductResource(ModelResource):
    class Meta:
        model = Product
class BotUserResource(ModelResource):
    class Meta:
        model = BotUserModel