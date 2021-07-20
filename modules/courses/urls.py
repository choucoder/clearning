from django.urls import path

from . import views


app_name = 'courses'

urlpatterns = [
	path('', views.CoursesView.as_view(), name='courses'),
	path('<str:course_id>/', views.CourseView.as_view(), name='single'),
	path('opening', views.CourseOpening.as_view(), name='opening'),
]