from django.contrib import admin
from .translation import CategoryTranslationOptions,ProductTranslationOptions
from modeltranslation.admin import TranslationAdmin
from import_export.admin import ImportExportModelAdmin
from .resources import *
from datetime import date
from django.utils.translation import gettext_lazy as _
# Register your models here.
from .models import *
from .utils import *

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
    list_display = ['picture','name','category','price','discount','taxminiy_vaqt']
    search_fields  = ['name','about','category__name']
    list_per_page = 10
    list_filter = ['discount','category']
    resource_classes = [ProductResource]



class OrderTableItemInline(admin.TabularInline):
    model = OrderTableItem

    def get_extra(self, request, obj=None, **kwargs):
        # Customize this number as needed
        return 3

class OrderTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'all_sum', 'time', 'status','total_unprepared_time')
    inlines = [OrderTableItemInline]

    def all_sum(self, obj):
        return obj.all_sum
    all_sum.short_description = 'Total Sum'

    def time(self, obj):
        return f"{obj.total_estimated_time} minut "
    time.short_description = 'Kutilgan vaqt'

    def total_unprepared_time(self, obj):
        return Sum_all_order_time()

    total_unprepared_time.short_description = 'Total Unprepared Time (mins)'

admin.site.register(OrderTable, OrderTableAdmin)
admin.site.register(OrderTableItem)

class TodayOrderFilter(admin.SimpleListFilter):
    title = _('Order Date')
    parameter_name = 'order_date'

    def lookups(self, request, model_admin):
        return (
            ('all', _('All')),
            ('today', _('Today')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            today = date.today()
            return queryset.filter(created_at__date=today)
        elif self.value() == 'all':
            return queryset
        return queryset

class Order_7foodAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id', 'full_name', 'phone', 'product', 'narxi', 'created_at', 'google_map_link', 'prepared', 'delivered', 'distance_from_me', 'taxminiy_vaqt', 'total_unprepared_time'
    )
    list_per_page = 30
    list_filter = (TodayOrderFilter,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Automatically filter to today's orders if 'order_date' filter is not set or is set to 'today'
        if 'order_date' not in request.GET or request.GET['order_date'] == 'today':
            today = date.today()
            return qs.filter(created_at__date=today)
        return qs

    def total_unprepared_time(self, obj):
        return total_estimated_time_undelivered_orders()

    total_unprepared_time.short_description = 'Total Unprepared Time (mins)'

    def mark_as_delivered(self, request, queryset):
        queryset.update(delivered=True)

    def mark_as_prepared(self, request, queryset):
        queryset.update(prepared=True)

    mark_as_delivered.short_description = "Mark selected orders as Delivered"
    mark_as_prepared.short_description = "Mark selected orders as Prepared"

    actions = [mark_as_delivered, mark_as_prepared]
admin.site.register(Order_7food, Order_7foodAdmin)

class Order_7foodSaboyAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id', 'full_name', 'phone', 'product', 'narxi', 'created_at',  'prepared', 'olib_ketildi','taxminiy_vaqt'
    )
    list_per_page = 30
    list_filter = (TodayOrderFilter,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Automatically filter to today's orders if 'order_date' filter is not set or is set to 'today'
        if 'order_date' not in request.GET or request.GET['order_date'] == 'today':
            today = date.today()
            return qs.filter(created_at__date=today)
        return qs

admin.site.register(Order_saboyfood, Order_7foodSaboyAdmin)









