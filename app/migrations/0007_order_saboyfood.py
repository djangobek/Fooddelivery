# Generated by Django 4.1.7 on 2024-06-28 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_product_taxminiy_vaqt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_saboyfood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(blank=True, null=True, verbose_name='Telegram ID')),
                ('full_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Full name')),
                ('phone', models.CharField(blank=True, max_length=150, null=True, verbose_name='Phone')),
                ('product', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Product')),
                ('narxi', models.IntegerField(blank=True, default=0, null=True, verbose_name='Sum')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('prepared', models.BooleanField(default=False, help_text='Agar buyurtma tayyorlangan bo`lsa chekboxni bosing !!!')),
                ('olib_ketildi', models.BooleanField(default=False, help_text='Agar buyurtma Olib ketilgan bo`lsa chekboxni bosing !!!', verbose_name='Olib ketildi')),
            ],
        ),
    ]
