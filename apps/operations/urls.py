from django.urls import path
from . import views

urlpatterns = [
    path("addfav/",views.addFav),
    path("getfav/",views.getFav),
    path("isfav/",views.isFav),
    path("setopinion/",views.setOpinion),
    path("getnum/",views.getNum),
    path("payorder/",views.payOrder),
    path("userorders/",views.userOrders),
]