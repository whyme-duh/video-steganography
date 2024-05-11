from django.contrib import admin
from django.urls import path
from imageSteg import views

urlpatterns = [
    path('steg/',views.encode_request ,name= 'image-steg'),
    path('decode-image/',views.decode_req ,name= 'image-decode'),
    path('image-steg-success/', views.image_sucess, name = 'image-success')
]
