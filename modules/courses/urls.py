from django.urls import path

from . import views


app_name = 'courses'

urlpatterns = [
	path('', views.CoursesView.as_view(), name='courses'),
	path('<str:course_id>/', views.CourseView.as_view(), name='single'),
	path('opening', views.CourseOpeningView.as_view(), name='opening'),
	path('enrollments/<str:enrollment_id>/students', views.CourseStudentsView.as_view(), name='students'),
	path('enrollments/<str:enrollment_id>/students-delete', views.CourseStudentDeleteView.as_view(), name='students-delete')
]