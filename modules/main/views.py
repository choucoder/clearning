from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from ..categories.models import Category
from ..courses.models import Course
from ..students.models import Student
from ..teachers.models import Teacher


class HomeView(LoginRequiredMixin, View):

	template_name = 'main/index.html'

	def get(self, request):
		context = {}
		context['categories'] = Category.objects.all()
		context['courses'] = Course.objects.all()
		context['teachers'] = Teacher.objects.all()
		return render(request, self.template_name, context)
