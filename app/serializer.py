from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
class BotUserSerializer(ModelSerializer):
    class Meta:
        model = BotUserModel
        fields = '__all__'
class TelegramChannelSerializer(ModelSerializer):
    class Meta:
        model = TelegramChannelModel
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
class SubCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = SubCategory
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer(many=True,read_only=True)
    products = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    shop = serializers.SerializerMethodField(read_only=True)
    product_id = serializers.SerializerMethodField(read_only=True)
    taxminiy_vaqt = serializers.SerializerMethodField(read_only=True)

    def get_shop(self, obj):
        return obj.shop

    def get_product_id(self, obj):
        return obj.product_id

    def get_taxminiy_vaqt(self, obj):
        return obj.product.taxminiy_vaqt if obj.product else None

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product', 'quantity', 'shop', 'taxminiy_vaqt']
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    products_count = serializers.SerializerMethodField(read_only=True)
    all_shop = serializers.SerializerMethodField(read_only=True)
    def get_products_count(self,obj):
        return obj.all_products
    def get_all_shop(self,obj):
        return obj.all_shop
    class Meta:
        model = Order
        fields = ['id','items','created','products_count','all_shop']


from rest_framework import serializers
from .models import *

class Order7foodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_7food
        fields = ['telegram_id', 'full_name', 'phone', 'product', 'narxi','taxminiy_vaqt']


class Order7foodSaboySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_saboyfood
        fields = ['telegram_id', 'full_name', 'phone', 'product', 'narxi','taxminiy_vaqt']