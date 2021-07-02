from django.db import models
from .models import *
from django.contrib import auth
from django.shortcuts import get_object_or_404, redirect, render
from haversine import haversine, Unit

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
    cafe_objects = Cafe.objects.all()
    
    return render(request, 'allcafe.html', {'data' : cafe_objects.order_by('distance')})

def review(request) :
    return render(request, 'review.html')

def takeout(request) :
    cafe_objects = Cafe.objects.all()
    cafe_objects = cafe_objects.filter(takeout_available=True)
    cafe_objects.order_by('distance')
    return render(request, 'takeout.html', {'data' : cafe_objects.order_by('distance')})


# def home(req): # 메인화면 로딩할때 사용
#     cafe_objects = Cafe.objects.all()
#     return render(req, '#', {'data' : cafe_objects})

##################################카페 CRUD######################################


def cafe_create(req): #카페 생성
    if req.mathod == 'POST':
        cafe_object = Cafe()
        cafe_object.title = req.POST['title']
        cafe_object.explanation = req.POST['explanation']
        cafe_object.reservation_available = req.POST['reservation']
        cafe_object.charge_available = req.POST['charge']
        cafe_object.total_seats = int(req.POST['total_seats'])
        cafe_object.congestion_status = int(req.POST['congestion_status'])
        #cafe_object.congestion_status = req.POST['congestion_status']
        # 위치랑 경도 받아오는 거 작업하기.(네이버 지도)
        cafe_object.thumbnail = req.POST['thumbnail']
        cafe_object.close_day = req.POST['close_day']
        cafe_object.cafe_phone_number = req.POST['phone_number']
        # if cafe_object.reservation_available:
        #     cafe_object.queuing_set.create(wating_number = 0, wating_team = 0, estimated_latency_default=10, estimated_latency=0)
        cafe_object.save()
        for img in req.FILES.getlist('#'): #여기에 이미지파일 받는 name 넣기
            photo = Image()
            photo.cafe = cafe_object
            photo.representative_image = img
            photo.save()
        return redirect('/cafe/'+str(cafe_object.id))
    return render(req, 'cafe_create.html')


def cafe_read(req, id): #카페 읽어오기

    cafe_object = get_object_or_404(Cafe, pk=id)
    reviews = cafe_object.review_set.all()
    if cafe_object.reservation_available:
        #queuing = cafe_object.queuing_set.all()
        # queuing = Queuing.objects.all()
        # queuing.filter(cafe=cafe_object)
        queuing = get_object_or_404(Queuing, cafe = cafe_object)
        content = {
        'data' : cafe_object,
        'reviews' :  reviews,
        'queuing' : queuing,
    }
    else:
        content = {
        'data' : cafe_object,
        'reviews' :  reviews,
    }
    
    return render(req, 'information.html', content)

def cafe_edit(req, id):  #카페 내용 수정
    cafe_object = get_object_or_404(Cafe, pk=id)
    if req.mathod == 'POST':
        cafe_object = Cafe()
        cafe_object.title = req.POST['title']
        cafe_object.explanation = req.POST['explanation']
        cafe_object.reservation_available = req.POST['reservation']
        cafe_object.charge_available = req.POST['charge']
        cafe_object.total_seats = int(req.POST['total_seats'])
        cafe_object.congestion_status = req.POST['congestion_status']
        # 위치랑 경도 받아오는 거 작업하기.
        cafe_object.operating_hour = req.POST['operating_hour']
        cafe_object.thumbnail = req.POST['thumbnail']
        cafe_object.save()
        return redirect('/cafe/'+str(id))
    return render(req, 'cafe_edit.html', {'data' : cafe_object})

def cafe_delete(req, id): #카페 삭제
    cafe_object = get_object_or_404(Cafe, pk=id)
    cafe_object.delete()
    return redirect('/')

def cafe_can_reservation(req):
    cafe_objects = Cafe.objects.all()
    cafe_objects = cafe_objects.filter(reservation_available=True)
    return render(req, 'allcafe.html', {'data' : cafe_objects.order_by('distance')})

def cafe_can_charge(req):
    cafe_objects = Cafe.objects.all()
    cafe_objects = cafe_objects.filter(charge_available=True)
    return render(req, 'allcafe.html', {'data' : cafe_objects.order_by('distance')})
##################################리뷰 CRUD######################################
def review_read(req, id):
    cafe_object = get_object_or_404(Cafe, pk=id)
    #reviews = cafe_object.review_set.all()
    content = {
        'data' : cafe_object,
        #'reviews' :  reviews,
    }
    return render(req, 'review.html', content)
    
def review_create(req, id):
    if req.method == 'POST':
        cafe_object = get_object_or_404(Cafe, pk=id)
        user = CustomUser.objects.get(user=req.user)
        cafe_object.reivew_set.create(writer = user.nickname, rating = req.POST['rating'], comment = req.POST['comment'])
        cafe_object.number_of_reivew += 1
        cafe_object.sum_of_reivew += int(req.POST['rating'])
        cafe_object.rating = int(cafe_object.sum_of_reivew/cafe_object.number_of_reivew)
    return redirect('/cafe/'+ str(id))

def review_delete(req,id):
    review_object = get_object_or_404(Review, pk=id)
    cafe_object = review_object.cafe
    cafe_object.number_of_reivew -=1
    cafe_object.sum_of_reivew -= review_object.rating
    cafe_object.rating = int(cafe_object.sum_of_reivew/cafe_object.number_of_reivew)
    review_object.delete()
    return redirect('/')

def review_modify(req, id):
    review_object = get_object_or_404(Review, pk=id)
    user = CustomUser.objects.get(user=req.user)
    if req.mathod == 'POST':
        review_object = Review()
        review_object.writer = user.nickname
        review_object.rating = req.POST['rating']
        review_object.comment = req.POST['comment']
        #return redirect('/cafe/'+str(id))
    #return render(req, 'cafe_edit.html', {'data' : cafe_object})

##################################쿠폰관련######################################

    def coupon_create(req,id):
        coupon_object = Coupon()
        coupon_object.user = req.user
        coupon_object.cafe = Cafe.objects.filter(id=id)
        coupon_object.save()
        
    def coupon_stamping(req, id):
        user_object = req.user
        cafe_object = Cafe.objects.filter(id=id)
        coupon_object = Coupon.objects.filter(user=user_object, cafe = cafe_object)
        coupon_object.stamp += 1
        if coupon_object.stamp == 12:
            coupon_object.free_coupon += 1
            coupon_object.stamp = 0

    def coupon_getPrize(req,id):
        user_object = req.user
        cafe_object = Cafe.objects.filter(id=id)
        coupon_object = Coupon.objects.filter(user=user_object, cafe = cafe_object)
        if coupon_object.free >= 1:
            coupon_object.free_coupon -= 1

##################################회원가입, 로그인, 로그아웃######################################
 
def signup_view(request):
	res_data = {}
	if request.method =='POST':
		if request.POST['password1'] == request.POST['password2']:
			user = CustomUser.objects.create_user(
				username = request.POST['username'], 
				password=request.POST['password1'], 
				nickname= request.POST['nickname']
			)
			auth.login(request, user)
			return redirect('home')
		else:
			res_data['error'] = '비밀번호가 다릅니다.'
	return render(request, 'signup.html', res_data)

    	
def login_view(request):
	res_data = {}
	username = "dlwnsgus07"
	password = "rdwg6867"
	user = auth.authenticate(request, username = username, password = password)
	if user is not None:
		auth.login(request, user)
		return redirect('home')
	else:
		res_data['error'] = '아이디나 비밀번호가 틀렸어요~'
    
    
#로그아웃
def logout_view(request):
	auth.logout(request)
	return redirect('home')


##################################대기열######################################

def add_queue(req, id): #대기열 추가인데. 유저당 대기번호를 하나씩 발급해 주어야 하나. 일단 프로토 타입임으로 임시로 보여주기식
    queueing_object = get_object_or_404(Queuing, pk = id)
    user = req.user
    cafe = queueing_object.cafe
    queueing_object.waiting_team += 1
    queueing_object.wating_number += 1
    PR = PersonalReservation()
    PR.queuing = queueing_object
    PR.user = user
    PR.wating_number = queueing_object.wating_number
    PR.save() 
    queueing_object.estimated_latency = queueing_object.waiting_team*queueing_object.estimated_latency_default
    queueing_object.save()
    content = {
        'cafe' : cafe,
        'personalReservation' :  PR,
        'queuing' : queueing_object,
    }
    
    return render(req, 'booking.html', content)

def cancel_queue(req,id):
    queueing_object = get_object_or_404(Queuing, pk = id)
    user = req.user
    PR = PersonalReservation()
    PR = PR.objects.filter(user=user)
    PR.delete()
    queueing_object.waiting_team -= 1
    queueing_object.estimated_latency = queueing_object.waiting_team*queueing_object.estimated_latency_default

def booking_read(req):
    user = req.user
    PR = get_object_or_404(PersonalReservation, user = user)
    queueing_object = PR.queuing
    cafe_object = queueing_object.cafe
    content = {
        'cafe' : cafe_object,
        'personalReservation' :  PR,
        'queuing' : queueing_object,
    }
    return render(req, 'booking.html', content)
###################################위치 정보에 따른 카페 필터##########################

def location_base_sorting(self, req):
    
    longitude = float(req.GET.get('longitude', None))
    latitude  = float(req.GET.get('latitude', None))
    position  = (latitude,longitude)
    condition = (
        Q(latitude__range  = (latitude - 0.01, latitude + 0.01)) |
        Q(longitude__range = (longitude - 0.015, longitude + 0.015))
    )
    convenience_cafes = Cafe.objects.filter(condition)
    convenience_cafes.order_by(self.number_of_reivew)
    near_convenience_cafes = [Cafe for Cafe in convenience_cafes
if haversine(position, (Cafe.lat, Cafe.lng)) <= 1]

    return render(req, '#', {'data' : near_convenience_cafes})