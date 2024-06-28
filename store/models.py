from django.db import models
from django.urls import reverse
from django.conf import settings
from colorfield.fields import ColorField



class Category(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=f'static/store/images/category')
    description = models.CharField(max_length=300)


    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_BOTH = 'b'
    GENDER_CHOICE = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_BOTH, 'Male & Female')
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='products')
    gender = models.CharField(choices=GENDER_CHOICE, max_length=1)
    sizes = models.ManyToManyField(to="store.Size", related_name="sizes")
    slug = models.SlugField(unique=True, allow_unicode=True, db_collation='utf8_persian_ci')
    price = models.PositiveIntegerField()
    new_price = models.PositiveIntegerField()
    description = models.TextField()
    inventory = models.IntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(default=0)
    available_colors = models.ManyToManyField(to="store.Color", related_name="colors")
    status = models.BooleanField(default=True)
    reviews = models.IntegerField(default=0)
    rating = models.CharField(max_length=6, null=True)
    shoe_upper = models.CharField(max_length=50, blank=True)
    shoe_soles = models.CharField(max_length=50, blank=True)
    insole = models.CharField(max_length=50, blank=True)


    def save(self, *args, **kwargs):
        self.new_price = round(self.price - self.price*self.discount/100)
        super(Product, self).save(*args, **kwargs)
    
    @property
    def discount_amount(self):
        return round(self.price*self.discount/100)



    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
    @property
    def all_sizes(self):
        list = [str(i) for i in self.sizes.all()]
        return ' - '.join(list)
    
    @property
    def all_colors(self):
        list = [i.farsi_name for i in self.available_colors.all()]
        return ' - '.join(list)


class Size(models.Model):
    size = models.CharField(max_length=2)


    def __str__(self):
        return self.size


class Color(models.Model):
    color = ColorField()
    name = models.CharField(max_length=20)
    farsi_name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Picture(models.Model):
    picture = models.ImageField(upload_to=f'static/store/images/')
    product = models.ForeignKey(Product, default=None, related_name='images', on_delete=models.PROTECT)

    def __str__(self):
        return self.picture.url
    

class Comment(models.Model):
    STARS_CHOICES = [('1', 'Very Bad'), ('2', 'Bad'), ('3', 'Normal'), ('4', 'Good'), ('5', 'Very Good')]
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    active = models.BooleanField(default=True)
    stars = models.CharField(choices=STARS_CHOICES, max_length=10, blank=True,)
        
    def __str__(self):
        return self.text


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=300)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self) -> str:
        return f'{self.user}'


class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'{self.customer} {self.product}'



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=700)
    is_paid = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    order_note = models.CharField(max_length=700, blank=True)
    new_total_price = models.IntegerField(default=0)
    total_discount = models.IntegerField(default=0)

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20)

    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    new_price = models.PositiveIntegerField()
    discount = models.IntegerField(default=0)

    @property
    def sub_total(self):
        return (self.quantity) * (self.price)
    
    @property
    def new_sub_total(self):
        return (self.quantity) * (self.new_price)
    
    @property
    def discount_amount(self):
        return round(self.quantity * self.price * self.discount /100)


    def __str__(self):
        return f'OrderItem {self.id}: {self.product} x {self.quantity} (price:{self.price})'
