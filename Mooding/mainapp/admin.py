from django.contrib import admin
from .models import *
# Register your models here.

class PhotoInline(admin.TabularInline):
    model = Image
class CafeAdmin(admin.ModelAdmin):
    inlines = [PhotoInline,]

admin.site.register(Cafe, CafeAdmin)
admin.site.register(Review)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Coupon)
admin.site.register(CustomUser)
admin.site.register(Queuing)
admin.site.register(PersonalReservation)