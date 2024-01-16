from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('',views.home ,name= 'home'),
    path('aboutus/',views.about_us ,name= 'aboutus'),
    path('encode/',views.encode,name= 'encode'),
    path('decode/',views.decode,name= 'decode'),
    path('decode-video/<int:id>',views.decode_vid_data,name= 'decode-video'),
    path('sucess/',views.sucess ,name= 'sucess'),
]
