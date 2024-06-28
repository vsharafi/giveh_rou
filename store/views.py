from .cart import Cart
from .compare import Compare
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from store.forms import CommentForm, CustomerForm, AddProductToCartForm, OrderRegisterForm
from store.models import Category, Color, Order, Product, Comment, Customer, OrderItem, Size, Wishlist


class HomePageView(TemplateView):
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context['top_rating'] = Product.objects.all().order_by("-rating")[:6]
        context['newest_products'] = Product.objects.all().order_by("-datetime_modified")[:6]
        context['special'] = Product.objects.filter(id="2").first()
        return context
    

class CategoryList(ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'


class CategoryProductList(ListView):
    model = Product
    template_name = 'products/product_list.html'
    paginate_by = 3
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_queryset(self):
        q = super().get_queryset()
        category = self.kwargs['category']
        q = q.filter(category__name=category)

        return q

    
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    paginate_by = 4
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["colors"] = Color.objects.all()
        context["sizes"] = Size.objects.all()
        # context["selected_categories"] = self.request.GET.getlist('category')
        return context

    def get_queryset(self):
        q = super().get_queryset()
        categories = self.request.GET.getlist('category')
        colors = self.request.GET.getlist('color')
        sizes = self.request.GET.getlist('size')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        sort = self.request.GET.get('sort')
        search = self.request.GET.get('search')
        filter_by_price = self.request.GET.get('filter_by_price')

        if categories:
            q = q.filter(category__name__in=categories)

        if colors:
            colors = list(Color.objects.filter(name__in=colors))
            q=q.filter(available_colors__in=colors).distinct()
        
        if sizes:
            sizes = list(Size.objects.filter(size__in=sizes))
            q=q.filter(sizes__in=sizes).distinct()

        if price_min and price_max:
            q = q.filter(new_price__lte=price_max, new_price__gt=price_min)

        if filter_by_price:
            p_min, p_max = filter_by_price.split(';')
            q = q.filter(new_price__lte=p_max, new_price__gt=p_min)
        
        if search:
            q = q.filter(name__icontains=search)

        if sort:
            if sort == 'rating':
                q = q.order_by("-rating")
            
            if sort == 'date':
                q = q.order_by("-datetime_modified")
            
            if sort == 'price':
                q = q.order_by("new_price")

            if sort == "price-desc":
                q = q.order_by("-new_price")

        return q
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        category = product.category
        # related_products = category.products.exclude(id=product.id)
        related_products = Product.objects.exclude(id=product.id)[:5]

        
        context = super().get_context_data(**kwargs)
        context['related_products'] = related_products
        context["colors"] = Color.objects.all()
        context['cart_form'] = AddProductToCartForm()
        context['form'] = CommentForm()
        return context


class CommentView(CreateView):
    model = Comment
    template_name = 'products/product_detail.html'
    form_class = CommentForm
    context_object_name = 'form'

    def get_queryset(self):
        q = super().get_queryset()
        return q.order_by("-datetime_created")

    def get_success_url(self):
        product = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return reverse("product_detail", kwargs={"slug": product.slug})
    
    def form_valid(self, form):
        product = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        comment_obj = form.save(commit=False)
        comment_obj.product = product
        comment_obj.author = self.request.user
        rating = float(product.rating)
        commet_star = float(comment_obj.stars)
        reviews = float(product.reviews)
        if comment_obj.stars:
            if product.rating == None:
                product.rating = comment_obj.stars
            else:

                rating = round((rating * reviews + commet_star)/(reviews + 1),1) 
                product.rating = rating
            product.reviews += 1
            product.save()
        messages.success(self.request, "Your comment was successfully submitted.")
        return super().form_valid(form)


@login_required
def profile_view(request):
    user = request.user
    customer = Customer.objects.get(user_id=user.id)
    form = CustomerForm(request.POST or None, instance=customer)
    # orders = user.orders.all()
    # orders = Order.objects.filter(user=user).prefetch_related('items__product')
    orders = Order.objects.filter(user=user).prefetch_related(
                                Prefetch(
                                    'items',
                                    queryset=OrderItem.objects.select_related('product')
                                         ))

    if request.method == "POST":
        if form.is_valid() and form.has_changed():
            edited_customer = form.save()
            user.first_name = edited_customer.first_name
            user.last_name = edited_customer.last_name
            user.save()
    return render(request, 'account/profile.html', {'form': form, 'orders': orders})


def cart_detail_view(request):
    cart = Cart(request)
    colors = Color.objects.all()
    for item in cart:
        item['product_update_quantity_form'] = AddProductToCartForm(initial={
            'inplace': True,
        })
    return render(request, 'products/cart_detail.html', {'cart': cart, 'colors': colors})


@require_POST
def add_to_cart_view(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    form = AddProductToCartForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        print('cleaned data: ', cleaned_data)
        size = cleaned_data['size']
        color = cleaned_data['color']
        quantity = (cleaned_data['quantity'])
        replace_current_quantity = cleaned_data['inplace']
        cart.add(product, size, color, quantity, replace_current_quantity)
    else:
        return redirect("product_detail", slug=product.slug)
    return redirect('cart_detail')


def remove_item_from_cart(request, cart_item):
    cart = Cart(request)
    cart.remove(cart_item)
    return redirect('cart_detail')


@require_POST
def clear_cart(request):
    cart = Cart(request)
    if len(cart) != 0:
        cart.clear()
    else:
        messages.warning(request, _("Your cart is already empty"))
    return redirect('product_list')

@login_required
def order_create_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, _("Your cart is empty. Please add some product to your cart."))
        return redirect("product_list")
    
    user = request.user
    customer = Customer.objects.get(user_id=user.id)

    order_form = OrderRegisterForm(initial={
                            'first_name': customer.first_name,
                            'last_name': customer.last_name,
                            'phone_number': customer.phone_number,
                            'address': customer.address,
                            })
    if request.POST:
        order_form = OrderRegisterForm(request.POST)
        if order_form.is_valid():

            with transaction.atomic():
                order_obj = order_form.save(commit=False)
                order_obj.user = request.user
                order_obj.save()
                data = order_form.cleaned_data

                customer.first_name=data['first_name']
                customer.last_name=data['last_name']
                customer.phone_number=data['phone_number']
                customer.address=data['address']
                customer.save()

                user.first_name=data['first_name']
                user.last_name=data['last_name']
                user.save()


                for item in cart:
                    product = item['product_obj']
                    OrderItem.objects.create(
                        order=order_obj,
                        product=product,
                        size=item['size'],
                        color=item['color'],
                        quantity=item['quantity'],
                        price=product.price,
                        new_price=product.new_price,
                        discount=product.discount,
                    )
                cart.clear()

                orders = user.orders.all()
                for order in orders:
                    total_price = 0
                    total_discount = 0
                    for item in order.items.all():
                        total_price += item.new_sub_total
                        total_discount += item.discount_amount
                    order.new_total_price = total_price
                    order.total_discount = total_discount
                    order.save()
                messages.success(request, _("Your order has successfully placed."))
    return render(request, 'orders/order_create.html', {'form': order_form})

    
def add_to_wishlist(request, pk):
    if not  request.user.is_active:
        messages.warning(request, _("Please login first for adding products to your wishlist."))
        return redirect('account_login')
    product = get_object_or_404(Product, pk=pk)
    user = request.user
    customer = Customer.objects.get(user_id=user.id)
    instance, created = Wishlist.objects.get_or_create(customer=customer, product=product)
    print(created)
    if not created:
        messages.warning(request, _("This product is already in your wishlist"))
    else:
        messages.success(request, _("Product has added to wishlist successfully"))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user = request.user
    customer = Customer.objects.get(user_id=user.id)
    item = Wishlist.objects.get(customer=customer, product=product)
    item.delete()
    messages.success(request, _('Product has removed from wishlist successfully.'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 

def compare_list_view(request):
    compare = Compare(request)
    compare_list = compare.compare_list
    if compare_list:
        product_list = Product.objects.filter(id__in=compare_list)
    else:
        product_list = []

    return render(request, 'products/compare_list.html', {"product_list": product_list})


def add_to_compare_list(request, pk):
    # product = get_object_or_404(Product, pk=pk)
    compare = Compare(request)
    compare.add(pk)
    return redirect('compare_list')


def remove_from_compare_list(request, pk):
    # product = get_object_or_404(Product, pk=pk)
    compare = Compare(request)
    compare.remove(pk)
    return redirect('compare_list')
