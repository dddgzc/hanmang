from django.urls import path
from . import views

urlpatterns = [
    path("userlogin/",views.userLogin),
    path("getuserinfo/",views.getUserInfo),
    path("userphone/",views.userPhone),
]