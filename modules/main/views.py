from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from ..categories.models import Category
from ..courses.models import Course, CourseOpening
from ..students.models import Student
from ..teachers.models import Teacher
from users.models import UserAccount


class HomeView(LoginRequiredMixin, View):

	template_name = 'main/index.html'

	def get(self, request):
		context = {}
		account = request.user

		if account.user_type in (UserAccount.SUBSCRIPTION, UserAccount.ADMIN):
			courses = CourseOpening.update_courses_status()
		
		elif account.user_type == UserAccount.TEACHER:
			teacher = Teacher.objects.filter(account=account).first()
			courses = CourseOpening.update_courses_status(teacher=teacher)
		else:
			# Asegurar que se traiga los cursos en los que se encuentra
			# ese estudiante
			courses = CourseOpening.update_courses_status()

		courses = courses.order_by('status', 'start_date')

		context['categories'] = Category.objects.all()
		context['courses'] = Course.objects.all()
		context['teachers'] = Teacher.objects.all()
		context['opened_courses'] = courses
		return render(request, self.template_name, context)
