from django.contrib import admin
from .models import User, Category, SubCategory, Product, Cart, Order, OrderProduct


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'telegram_id')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'title',)



class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'structure')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_title', 'get_price', 'count', 'price')
    readonly_fields=('price',)
    def get_title(self, obj):
        return obj.product.title

    def get_price(self, obj):
        return obj.product.price
    get_title.short_description = 'Title'
    get_price.short_description = 'Mahsulot narxi'


class ChildInline(admin.TabularInline):
    model = OrderProduct


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'total', 'status', 'created')
    inlines = [
        ChildInline,
    ]
    

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)