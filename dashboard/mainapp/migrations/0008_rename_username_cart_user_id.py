# Generated by Django 4.0.4 on 2022-04-20 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_cart_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='username',
            new_name='user_id',
        ),
    ]
