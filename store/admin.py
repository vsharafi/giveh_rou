from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from .models import Category, Customer, Picture, Product, Comment, Size, Color, Order, OrderItem, Wishlist


admin.site.site_header = 'Giveh Rou'



class PictureInline(admin.TabularInline):
    model = Picture
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category', 'new_price', 'description', 'slug', 'datetime_modified', 'id']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PictureInline, CommentInline]


@admin.register(Customer)
class CustomerAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['user','phone_number', 'address', 'first_name', 'last_name', 'id']


admin.site.register(Category)

admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Comment)
admin.site.register(Wishlist)




class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'size', 'color', 'quantity', 'price',]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'is_paid', 'datetime_created']
    inlines = [OrderItemInline, ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'size', 'color', 'quantity', 'price']
