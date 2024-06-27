from django.contrib import admin
from .translation import CategoryTranslationOptions,ProductTranslationOptions
from modeltranslation.admin import TranslationAdmin
from import_export.admin import ImportExportModelAdmin
from .resources import *
# Register your models here.
from .models import *
@admin.register(BotUserModel)
class BotUserAdmin(ImportExportModelAdmin):
    list_display = ['name','telegram_id','language','added']
    list_editable = ['language','name']
    list_display_links = ['telegram_id']
    list_per_page = 10
    resource_classes = [BotUserResource]
@admin.register(TelegramChannelModel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ['channel_id','channel_name','channel_members_count']
    list_display_links = ['channel_name']
    list_per_page = 10
@admin.register(Location)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ['user','latitude','longitude']
    list_per_page = 10
@admin.register(Category)
class CategoryAdmin(TranslationAdmin,ImportExportModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 10
    resource_classes = [CategoryResource]
@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin,ImportExportModelAdmin):
    list_display = ['name','category']
    search_fields = ['name','category__name']
    list_per_page = 10
@admin.register(Product)
class ProductAdmin(TranslationAdmin,ImportExportModelAdmin):
    list_display = ['picture','name','category','price','discount']
    search_fields  = ['name','about','category__name']
    list_per_page = 10
    list_filter = ['discount','category']
    resource_classes = [ProductResource]
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','all_shop','all_products']
    list_per_page = 10
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity','shop']
    list_per_page = 10


class Order_7foodAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'full_name', 'phone', 'product', 'narxi', 'created_at', 'google_map_link', 'prepared', 'delivered')
    list_per_page = 30
admin.site.register(Order_7food, Order_7foodAdmin)