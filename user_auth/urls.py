from django.urls import path
from user_auth.views import UserProfile, Signup, PasswordChange, PasswordChangeDone,EditProfile
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('profile/', UserProfile, name='profile'),
    path('profile/edit', EditProfile, name='editprofile'),
    path('signup/', Signup, name='signup'),
    path('changepassword/', PasswordChange, name='change_password'),
    path('changepassword/done', PasswordChangeDone, name='change_password_done'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(),{'next_page': 'index'},name='logout'),
]
