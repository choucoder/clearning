from django.urls import path

from . import views


app_name = 'teachers'

urlpatterns = [
	path('', views.TeachersView.as_view(), name='list'),
	path('<str:teacher_id>/', views.TeacherView.as_view(), name='single'),
]