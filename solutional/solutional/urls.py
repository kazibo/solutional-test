"""solutional URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from mainapp.views import products_view, orders_view, orders_single_view, order_products_view, \
    order_products_single_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', products_view),
    path('api/orders/', orders_view),
    path('api/orders/<order_id>/', orders_single_view),
    path('api/orders/<order_id>/products/', order_products_view),
    path('api/orders/<order_id>/products/<order_product_id>/', order_products_single_view),
]
