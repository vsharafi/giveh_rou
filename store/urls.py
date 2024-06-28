from django.urls import path

from store import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),
    path('category', views.CategoryList.as_view(), name="category_list"),
    path('<category>', views.CategoryProductList.as_view(), name="category_product_list"),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path("products/<slug>/", views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug>/comment', views.CommentView.as_view(), name='comment_create'),
    path('accounts/profile/', views.profile_view, name='account_profile'),
    path('cart/', views.cart_detail_view, name='cart_detail'),
    path('cart/add/<int:pk>/', views.add_to_cart_view, name="cart_add"),
    path('cart/remove/<int:cart_item>/', views.remove_item_from_cart, name='cart_remove'),
    path('clear/', views.clear_cart, name='cart_clear'),
    path('order/create/', views.order_create_view, name='order_create'),
    path('wishlist/add/<int:pk>/', views.add_to_wishlist, name='wishlist_add'),
    path('wishlist/remove/<int:pk>/', views.remove_from_wishlist, name='wishlist_remove'),
    path('comparison/', views.compare_list_view, name="compare_list"),
    path('comparison/add/<int:pk>/', views.add_to_compare_list, name="compare_add"),
    path('comparison/remove/<int:pk>/', views.remove_from_compare_list, name="compare_remove"),



    
]

