from django.db import models
from django.db import models
from django.utils.html import format_html
from math import radians, sin, cos, sqrt, atan2
# Create your models here.
class BotUserModel(models.Model):
    languages = (
        ('uz',"O'zbek",),
        ('en',"English")
    )
    name = models.CharField(max_length=300,null=True,blank=True,verbose_name="Full Name",help_text="Enter full name")
    telegram_id = models.CharField(max_length=100,unique=True,verbose_name="Telegram ID",help_text="Enter telegram id")
    language = models.CharField(max_length=5,default='uz',choices=languages,verbose_name="Language",help_text="Choose language")
    language = models.CharField(max_length=4, default='uz', verbose_name="Language", help_text="Enter language")
    phone = models.CharField(max_length=20, verbose_name="Phone number", help_text="Enter phone number", null=True,
                          blank=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=200, null=True, blank=True,)
    def __str__(self):
        if self.name:
            return f"{self.name}"
        else:
            return f"User with ID:{self.telegram_id}"
    class Meta:
        verbose_name = 'Bot User'
        verbose_name_plural='Bot Users'
class TelegramChannelModel(models.Model):
    channel_id = models.CharField(max_length=150,verbose_name="Channel ID",help_text="Enter channel id",unique=True)
    channel_name = models.CharField(max_length=300,verbose_name="Channel Name",help_text="Enter channel name",null=True,blank=True)
    channel_members_count = models.CharField(max_length=200,null=True,blank=True,verbose_name="Channel Memers Count",help_text="Enter channel members count")
    def __str__(self):
        return f"Channel: {self.channel_id}"
    class Meta:
        verbose_name = 'Telegram Channel'
        verbose_name_plural = 'Telegram Channels'


from main import manzil
class Location(models.Model):
    user = models.ForeignKey(BotUserModel, on_delete=models.CASCADE, verbose_name="Bot User", to_field='telegram_id')
    latitude = models.CharField(max_length=50, verbose_name="Latitude", null=True, blank=True)
    longitude = models.CharField(max_length=50, verbose_name="Longitude", null=True, blank=True)

    def __str__(self) -> str:
        if self.latitude and self.longitude:
            return manzil(latitude=self.latitude, longitude=self.longitude)
        else:
            return "Manzil"

    class Meta:
        db_table = "Location"
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Category", help_text="Enter category")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name="Subcategory", help_text="Enter subcategory")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category",
                                 help_text="Choose category", null=True, blank=True, related_name='subcategory')

    def __str__(self):
        return self.name
    class Meta:
        db_table = "SubCategory"
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"


from django.utils.html import format_html


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Product", help_text="Enter product name", null=True,
                            blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category",
                                 help_text="Choose category", related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='Subcategory', related_name='products')
    image = models.ImageField(upload_to='my-images', verbose_name="Image", help_text='Upload image', null=True,
                              blank=True)
    about = models.TextField(verbose_name="About", null=True, blank=True)
    price = models.IntegerField(verbose_name="Price", help_text="Enter price", default=0)
    discount = models.IntegerField(verbose_name="Discount", help_text="Enter discount", default=0)
    taxminiy_vaqt = models.IntegerField(default = 2, help_text="Tayyorlash uchun ketadigan  taxminiy vaqtni Kiriting !!", blank=True, null=True)
    def __str__(self):
        # print(self.image.url)
        if self.name:
            return self.name
        else:
            return 'Mahsulot'

    @property
    def picture(self):
        return format_html('<img src="{}" width="50" height="50" style="border-radius:50%"'.format(self.image.url))

    class Meta:
        db_table = "Product"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Order(models.Model):
    user = models.ForeignKey(BotUserModel, on_delete=models.CASCADE, verbose_name="Bot User", to_field='telegram_id')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user.name:
            return self.user.name
        else:
            return "Buyurtma"

    @property
    def all_products(self):
        return sum([item.quantity for item in self.items.all()])

    @property
    def all_shop(self):
        return sum([item.shop for item in self.items.all()])

    class Meta:
        db_table = "Order"
        verbose_name = "Order"
        verbose_name_plural = "Order"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Order", related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.IntegerField(default=1, verbose_name="Quantity")

    def __str__(self):
        return 'Xarid'

    @property
    def shop(self):
        if self.product.discount:
            return (int(self.product.price) - (self.product.discount)) * int(self.quantity)
        else:
            return int(self.product.price) * int(self.quantity)

    @property
    def product_id(self):
        return self.product.id

    class Meta:
        db_table = "OrderItem"
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"



class Order_7food(models.Model):
    telegram_id = models.IntegerField(verbose_name="Telegram ID", null=True, blank=True)
    full_name = models.CharField(max_length=150, verbose_name="Full name", null=True, blank=True)
    phone = models.CharField(max_length=150, verbose_name="Phone", null=True, blank=True)
    product = models.CharField(verbose_name="Product", max_length=1000, null=True, blank=True)
    narxi = models.IntegerField(verbose_name="Sum", default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    prepared = models.BooleanField(default=False, help_text="Agar buyurtma tayyorlangan bo`lsa chekboxni bosing !!!")
    delivered = models.BooleanField(default=False, verbose_name="Delivered")
    taxminiy_vaqt = models.IntegerField(verbose_name="Taxminiy Vaq", default = 2, null=True, blank=True)
    def google_map_link(self):
        try:
            user = BotUserModel.objects.get(telegram_id=self.telegram_id)
            if user.latitude and user.longitude:
                url = f"https://www.google.com/maps/search/?api=1&query={user.latitude},{user.longitude}"
                return format_html(f'<a href="{url}" target="_blank">View on Map</a>')
            else:
                return "No location available"
        except BotUserModel.DoesNotExist:
            return "User not found"

    google_map_link.short_description = 'Google Map Link'

    @property
    def distance_in_meters(self):
        try:
            user = BotUserModel.objects.get(telegram_id=self.telegram_id)
            my_latitude = 39.67520758749987
            my_longitude = 66.9268985761301
            if user.latitude and user.longitude:
                lat1, lon1 = radians(my_latitude), radians(my_longitude)
                lat2, lon2 = radians(float(user.latitude)), radians(float(user.longitude))

                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = 6371 * c  # Distance in kilometers

                # Convert distance to meters and round to 3 decimal places
                distance_meters = round(distance * 1000)
                return distance_meters
            else:
                return None
        except BotUserModel.DoesNotExist:
            return None

    def distance_from_me(self):
        distance_meters = self.distance_in_meters
        return f'{distance_meters} meters' if distance_meters is not None else None


    def __str__(self):
        if self.full_name:
            return self.full_name
        else:
            return "Order"

    class Meta:
        db_table = "Order_7food"
        verbose_name = "Order"
        verbose_name_plural = "Orders"



class Order_table(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")




class OrderTable(models.Model):
    name = models.CharField(max_length=300, default="foydalanuvchi", verbose_name="Name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    products = models.ManyToManyField(Product, through='OrderTableItem', related_name='order_tables', verbose_name="Products")
    status = models.BooleanField(default=False, verbose_name="Status",
                                 help_text="Tayyorlanga bo`lsa statusni belgilab keting !!!")
    def __str__(self):
        if self.name:
            return f"Order by {self.name}"


    @property
    def all_sum(self):
        total_sum = sum(item.total_price for item in self.items.all())
        return total_sum

    @property
    def total_estimated_time(self):
        total_time = sum(item.estimated_time for item in self.items.all())
        return total_time
    class Meta:
        db_table = "OrderTable"
        verbose_name = "Order Table"
        verbose_name_plural = "Order Tables"


class OrderTableItem(models.Model):
    order_table = models.ForeignKey(OrderTable, on_delete=models.CASCADE, related_name='items', verbose_name="Order Table")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.IntegerField(default=1, verbose_name="Quantity")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    @property
    def estimated_time(self):
        return self.product.taxminiy_vaqt * self.quantity

    class Meta:
        db_table = "OrderTableItem"
        verbose_name = "Order Table Item"
        verbose_name_plural = "Order Table Items"


class Order_saboyfood(models.Model):
    telegram_id = models.IntegerField(verbose_name="Telegram ID", null=True, blank=True)
    full_name = models.CharField(max_length=150, verbose_name="Full name", null=True, blank=True)
    phone = models.CharField(max_length=150, verbose_name="Phone", null=True, blank=True)
    product = models.CharField(verbose_name="Product", max_length=1000, null=True, blank=True)
    narxi = models.IntegerField(verbose_name="Sum", default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    prepared = models.BooleanField(default=False, help_text="Agar buyurtma tayyorlangan bo`lsa chekboxni bosing !!!")
    olib_ketildi = models.BooleanField(default=False, verbose_name="Olib ketildi", help_text="Agar buyurtma Olib ketilgan bo`lsa chekboxni bosing !!!" )
    taxminiy_vaqt = models.IntegerField(verbose_name="Taxminiy Vaq", default = 2, null=True, blank=True)


    def __str__(self):
        if self.full_name:
            return self.full_name
        else:
            return "Order"
