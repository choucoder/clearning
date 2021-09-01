from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
	path('login', views.LoginView.as_view(), name='login'),
	path('logout', views.LogoutView.as_view(), name='logout'),
	path('register', views.AccountRegisterView.as_view(), name='register'),
	path('forgot-password', views.ForgotPasswordView.as_view(), name='forgot-password'),
	path('teacher/register', views.TeacherRegisterView.as_view(), name='teacher-register'),
	path('', views.AccountsView.as_view(), name='list'),
]