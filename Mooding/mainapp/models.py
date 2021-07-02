
from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import Model, ModelBase
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import CharField
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=100, blank=True, null=True) #리뷰에 사용될 닉네임이 저장될 곳
    steamed_list = models.IntegerField(blank=True, null=True) #찜한 카페 PK인 id를 저장할 곳
class Cafe(models.Model): # 카페 클래스
    Relax = 0
    Average = 1
    Congestion = 2
    CONGESTION_CHOICE =(
        (Relax, '여유'),
        (Average, '보통'),
        (Congestion, '혼잡')
    )
    WEEK =(
        ('월요일', '월요일'),
        ('화요일', '화요일'),
        ('수요일', '수요일'),
        ('목요일', '목요일'),
        ('금요일', '금요일'),
        ('토요일', '토요일'),
        ('일요일', '일요일'),
    )
    #id = models.AutoField(primary_key=True) # 카페 아이디(프라이머리 키)
    title = models.CharField(max_length=100) # 카페이름
    explanation = models.TextField(blank=True) # 카페 설명
    reservation_available = models.BooleanField() #예약 가능여부
    charge_available = models.BooleanField() # 충전 가능 여부
    takeout_available = models.BooleanField()# 테이크 아웃 가능 여부
    total_seats = models.SmallIntegerField() # 총 좌석 수
    used_seats = models.SmallIntegerField(null=True) # 사용하고 있는 좌석 수
    unused_seats = models.SmallIntegerField(null=True) # 미사용 좌석 수
    congestion_status = models.SmallIntegerField(default=0, choices=CONGESTION_CHOICE) # 혼잡여부(숫자료 표현 0, 1, 2) choice 활용
    lat = models.FloatField(default=0) #위도 (영빈이형 말대로 네이버 GPS사용하기.)(영빈이형 말로는 위도 경도는 정수가 아닌 문자열로 받아서 소수점 변환이 좋음)
    lng = models.FloatField(default=0)#경도
    thumbnail = models.ImageField(default ="#") #썸네일 이미지
    operating_hour = models.TextField(blank=True) #운영시간
    close_day = models.TextField(blank=True, choices=WEEK)  #휴무일
    cafe_phone_number = models.CharField(max_length=14, blank=True) #카페 전화번호
    rating = models.FloatField(blank=True) # 카페 별점 점수를 저장하는 곳
    number_of_reivew = models.IntegerField(default=0) # 별점 평균을 저장하기 위해 리뷰 수 저장
    sum_of_reivew = models.IntegerField(default=0) # 별점 평균을 저장하기 위해 리뷰레이팅의 합 저장
    distance = models.FloatField(default=0)

    def __str__(self):
        return self.title
class Review(models.Model): # 리뷰 서비스
    Star1 = 1
    Star2 = 2
    Star3 = 3
    Star4 = 4
    Star5 = 5
    RATING =(
        (Star1, '1점'),
        (Star2, '2점'),
        (Star3, '3점'),
        (Star4, '4잠'),
        (Star5, '5점'),
    )
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE) # 카페 하나에 종속
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    writer = models.CharField(max_length=20)# 작성자
    rating = models.SmallIntegerField(default=5, choices=RATING) # 별점을 사용자로부터 입력받기 위해 사용
    comment = models.TextField() #리뷰내용
    def __str__(self):
        return self.cafe.title


class Product(models.Model): #판매할 상품
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE) # 카페 하나에 종속
    title = models.CharField(max_length=100) #상품 이름
    price = models.IntegerField() # 상품가격
    reduced_price = models.IntegerField()#할인가격
    out_of_stock = models.BooleanField() # 매진여부
    

class Image(models.Model): # 이미지 
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE) #카페 종속
    representative_image = models.ImageField() #카페 대표 이미지

class Coupon(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE) #카페, 유저에 종속되도록
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stamp = models.IntegerField(default=0) # 도장
    prizes = models.TextField(default="아메리카노 1잔") #상품
    free_coupon = models.IntegerField(default=0) # 도장을 다 채웠을 때 주어지는 상품권
   
class Queuing(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    wating_number = models.IntegerField(default=1)
    waiting_team = models.IntegerField(default=0)
    estimated_latency_default = models.IntegerField(default=30)
    estimated_latency = models.IntegerField(default=0)
    def __str__(self):
        return self.cafe.title
#대기열 개인별 대기표와 카페별 대기열로 모델 나눠서 다시 만들기 
class PersonalReservation(models.Model):
    queuing = models.ForeignKey(Queuing, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wating_number = models.IntegerField(blank=True)
    time = models.DateTimeField(auto_now=True)