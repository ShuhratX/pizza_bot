from django.db import models


class User(models.Model):
    id          = models.AutoField(primary_key=True)
    full_name   = models.CharField(verbose_name="Ism", max_length=100)
    username    = models.CharField(verbose_name="Telegram username", max_length=100, null=True)
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID', unique=True, default=1)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.full_name


class Category(models.Model):
    title = models.CharField(verbose_name="Kategoriya nomi", max_length=150)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name="Kategoriya", on_delete=models.CASCADE)
    title    = models.CharField(verbose_name="Kategoriya nomi", max_length=150)

    class Meta:
        db_table = "subcategories"

    def __str__(self):
        return self.title


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, verbose_name="Subkategoriya", on_delete=models.CASCADE)
    title     = models.CharField(verbose_name="Maxsulot nomi", max_length=150)
    price     = models.PositiveIntegerField(verbose_name="Narxi")
    structure = models.TextField(verbose_name="Tarkibi")
    image     = models.ImageField(verbose_name="Rasm")

    class Meta:
        db_table = "products"
    
    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="Foydalanuvchi", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Mahsulot", on_delete=models.CASCADE)
    count   = models.CharField(verbose_name="Maxsulot soni", max_length=10)
    price   = models.PositiveIntegerField(verbose_name="Narxi", null=True, blank=True)

    class Meta:
        db_table = "cart"
    
    def __str__(self):
        return self.product.title
    
    def save(self, *args, **kwargs):
        self.price = self.product.price * int(self.count)
        return super(Cart, self).save(*args, **kwargs)
    
    
class Order(models.Model):
    STATUS_CHOICE = (
        ('new','new'),
        ('processing','processing'),
        ('finished','finished'),
        ('cancel','cancel')
    )
    user         = models.ForeignKey(User, verbose_name="Foydalanuvchi", on_delete=models.CASCADE)
    status       = models.CharField(choices=STATUS_CHOICE, max_length=255, default='new')
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    name         = models.CharField(max_length=150, verbose_name="Ismi")
    total        = models.PositiveIntegerField(null=True, blank=True, verbose_name="Jami")
    created      = models.DateTimeField(auto_now_add=True, verbose_name="Vaqti")

    def __str__(self):
        return str(self.phone_number)


class OrderProduct(models.Model):
    class Meta:
        ordering = ('-id',)
        
    order   = models.ForeignKey(Order, verbose_name="Buyurtma", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Maxsulot", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, verbose_name="Soni")

    def __str__(self) -> str:
        return self.product.title