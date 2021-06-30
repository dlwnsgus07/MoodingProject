"""mooding URL Configuration

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

import mainapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.views.intro, name = 'intro'),
    path('home/', mainapp.views.home, name = 'home'),
    path('like', mainapp.views.like, name = 'like'),
    path('reserve', mainapp.views.reserve, name = 'reserve'),
    path('mypage', mainapp.views.mypage, name = 'mypage'),
    path('coupon', mainapp.views.coupon, name = 'coupon'),
    path('information', mainapp.views.information, name = 'information'),
    path('booking', mainapp.views.booking, name = 'booking'),
    path('allcafe', mainapp.views.allcafe, name = 'all_cafe'),
    path('review', mainapp.views.review, name = 'review'),
    path('takeout', mainapp.views.takeout, name='takeout'),
]
