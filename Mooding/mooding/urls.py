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
from django.contrib.auth import login
from django.contrib import admin
from django.urls import path

import mainapp.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.views.intro, name = 'intro'),
    path('home/', mainapp.views.home, name = 'home'),
    path('like', mainapp.views.like, name = 'like'),
    path('reserve', mainapp.views.booking_read, name = 'reserve'),
    path('mypage', mainapp.views.mypage, name = 'mypage'),
    path('coupon', mainapp.views.coupon, name = 'coupon'),
    path('information/<int:id>', mainapp.views.cafe_read, name = 'information'),
    path('booking/<int:id>', mainapp.views.add_queue, name = 'booking'),
    path('allcafe', mainapp.views.allcafe, name = 'all_cafe'),
    path('review/<int:id>', mainapp.views.review_read, name = 'review'),
    path('takeout', mainapp.views.takeout, name='takeout'),
    path('reservation_available', mainapp.views.cafe_can_reservation, name ='reservation_available'),
    path('charge_available', mainapp.views.cafe_can_charge, name ='charge_available'),
    path('login', mainapp.views.login_view, name='login'),
]   

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)