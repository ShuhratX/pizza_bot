# Generated by Django 4.0.4 on 2022-04-19 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Narxi'),
        ),
    ]
