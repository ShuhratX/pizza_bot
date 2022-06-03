# Generated by Django 4.0.4 on 2022-04-23 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_alter_cart_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'new'), ('processing', 'processing'), ('finished', 'finished'), ('cancel', 'cancel')], default='new', max_length=255)),
                ('phone_number', models.CharField(max_length=20, verbose_name='Telefon raqami')),
                ('name', models.CharField(max_length=150, verbose_name='Ismi')),
                ('total', models.PositiveIntegerField(blank=True, null=True, verbose_name='Jami')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Vaqti')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.user', verbose_name='Foydalanuvchi')),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user_id',
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainapp.user', verbose_name='User_id'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Soni')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.order', verbose_name='Buyurtma')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Maxsulot')),
            ],
        ),
    ]
