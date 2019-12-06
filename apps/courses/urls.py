from django.urls import path
from . import views

urlpatterns = [
    path("courselist/",views.courseList),
    path("getcourse/",views.getCourse),
    path("getcoursetype/",views.getCourseType),
    path("getcoursebyclassic/",views.getCourseByClassic),
    path("getcoursecomment/",views.getCourseComment)
]