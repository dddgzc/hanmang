from django.urls import path
from . import views

urlpatterns = [
    path("getcourse/",views.getCourse),
    path("getcoursetype/",views.getCourseType),
    path("getcoursebyclassic/",views.getCourseByClassic),
    path("getcoursecomment/",views.getCourseComment),
    path("itemsLoop/",views.itemsLoop),
    path("getpagecourses/",views.getPageCourses),
    path("getcourselist/",views.getCourseList),
]