from django.urls import path
from . import views

urlpatterns = [
    path("addfav/",views.addFav),
    path("getfav/",views.getFav),
    path("isfav/",views.isFav)

]