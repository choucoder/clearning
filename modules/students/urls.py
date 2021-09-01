from django.urls import path

from . import views

app_name = 'students'

urlpatterns = [
	path('', views.StudentsView.as_view(), name='list'),
	path('enrollments/<str:enrollment_id>', views.EnrollmentView.as_view(), name='students-enrollments'),
	path('enrollments/<str:enrollment_student_id>/notes', views.EnrollmentNotesView.as_view(), name='students-enrollments-notes'),
	path('enrollments/<str:enrollment_id>/attendances', views.EnrollmentAttendancesView.as_view(), name='students-enrollments-attendances'),
	path('enrollments/<str:enrollment_id>/payments', views.EnrollmentPaymentsView.as_view(), name='students-enrollments-payments'),
]