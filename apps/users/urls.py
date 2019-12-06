from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.login),
    path("test/",views.test),
    path("checkreg/",views.checkreg),
    path("userinfo/",views.getUserInfo)
]