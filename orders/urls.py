from django.urls import path, include
from notifications import urls as notifications_urls

from . import views

from django.conf.urls import handler404
from orders.views import page_not_found_404

app_name = 'orders'

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login", views.log_in, name="login"),
    path("logout", views.log_out, name="logout"),
    path("menu", views.menu, name="menu"),
    path("basket", views.basket, name="basket"),
    path("place", views.place, name="place"),
    path("account", views.account, name="account"),
    path("account/filter/<filter_by>", views.filter, name="filter"),
    path('user_orders', views.user_orders, name='user_orders'),
    path('notifications/', include(notifications_urls)),
    path("directions", views.directions, name="directions"),
    path("contact", views.contact, name="contact"),
]

handler404 = page_not_found_404