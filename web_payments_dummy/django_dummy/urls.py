"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include
from django.urls import path, re_path

from web_payments.django import urls as web_payment_urls
from .views import PaymentView, PayObView, SelectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("payment/", include(web_payment_urls)),
    re_path("^payob/(?P<id>[0-9]+)/$", PayObView.as_view(), name="paymentob"),
    re_path(
        "^form/(?P<id>[0-9]+)/$", PaymentView.as_view(), name="payment-form"
    ),
    path("", SelectView.as_view(), name="select-form"),
]
