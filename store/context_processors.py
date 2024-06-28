from .cart import Cart
from .models import Category, Color, Customer, Size, Wishlist


def cart(request):
    categories = Category.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        wishlist = Wishlist.objects.filter(customer=customer)
    else:
        wishlist = ''

    return {'cart': Cart(request), 'categories': categories, 'colors': colors, 'sizes': sizes, "wishlist": wishlist}