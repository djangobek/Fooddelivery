from django.db import models
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

    def __str__(self):
        if self.full_name:
            return self.full_name
        else:
            return "Order"

    class Meta:
        db_table = "Order_7food"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

