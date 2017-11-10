"""program0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from account import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^login_view', views.login_view,name="login_view"),
    url(r'^logout_view', views.logout_view,name="logout_view"),
    url(r'^register', views.register,name="register"),
    url(r'^admin/', admin.site.urls),
    url(r'^home', views.home,name="home"),
    url(r'^user_info', views.user_info,name="user_info"),
    url(r'^upload', views.upload,name="upload"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
