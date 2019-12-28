"""hanmang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve
from .settings import MEDIA_ROOT
import xadmin

urlpatterns = [
    path('xadmin/',xadmin.site.urls),
    path('user/',include('apps.users.urls')),
    path('organizations/',include('apps.organizations.urls')),
    path('course/',include('apps.courses.urls')),
    path('operations/',include('apps.operations.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    ##配置文件上传之后的访问路径
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
]
