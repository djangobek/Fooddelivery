# Generated by Django 4.1.7 on 2024-06-28 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_ordertable_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_7food',
            name='taxminiy_vaqt',
            field=models.IntegerField(blank=True, default=2, null=True, verbose_name='Taxminiy Vaq'),
        ),
        migrations.AddField(
            model_name='order_saboyfood',
            name='taxminiy_vaqt',
            field=models.IntegerField(blank=True, default=2, null=True, verbose_name='Taxminiy Vaq'),
        ),
    ]
