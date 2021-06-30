from django.shortcuts import render

# Create your views here.
def intro(request) :
    return render(request, 'intro.html')

def home(request) :
    return render(request, 'home.html')

def like(request) :
    return render(request, 'like.html')

def reserve(request) :
    return render(request, 'reserve.html')

def mypage(request) :
    return render(request, 'mypage.html')

def coupon(request) :
    return render(request, 'coupon.html')

def information(request) :
    return render(request, 'information.html')

def booking(request) :
    return render(request, 'booking.html')

def allcafe(request) :
    return render(request, 'allcafe.html')

def review(request) :
    return render(request, 'review.html')

def takeout(request) :
    return render(request, 'takeout.html')