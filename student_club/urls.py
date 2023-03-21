"""student_club URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from user_auth.views import UserProfile,ProfileFollow

urlpatterns = [
    path('admin/feedback-report', include('admin.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user_auth.urls')),
    path('post/', include('post.urls')),
    path('inbox/', include('message.urls')),
    path('<username>/', UserProfile, name="profile"),
    path('<username>/follow/<option>', ProfileFollow, name="follow"),
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.index_title = "StudentClub"
admin.site.site_header = "StudentClub Administration"
