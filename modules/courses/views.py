from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .forms import CourseCreateForm, CourseOpeningForm
from .models import Course


class CoursesView(LoginRequiredMixin, View):

	form = CourseCreateForm

	def post(self, request):
		context = {}

		try:
			form = self.form(request.POST)
			if form.is_valid():
				form = form.cleaned_data
				categories = form.pop('categories')
				categories = categories.split(',')

				course = Course(**form)
				course.save()

				for name in categories:
					cat = Category.objects.get(name=name)
					course.categories.add(cat)

				course.reload()

				context['status'] = 201
				context['message'] = f"El curso {course.name} ha sido registrado con exito"
				context['data'] = course.to_json()

			else:
				context['status'] = 400
				context['message'] = "Datos ingresados no son validos"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)


class CourseView(View):

	def get(self, request, course_id):

		context = {}
		try:
			course = Course.objects.get(id=course_id)
			context['status'] = 200
			context['message'] = f"Curso {course.name}"
			context['data'] = course.to_json()

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)


	def put(self, request, course_id):
		pass

	def delete(self, request, course_id):
		pass


class CourseOpening(View):

	form = CourseOpeningForm

	def post(self, request):
		context = {}

		try:
			form = self.form(request.POST)
			pprint(request.POST)

			if form.is_valid():
				form = form.cleaned_data
				course, teacher = None, None

				if not 'course_register_checkbox' in form:
					course = Course.objects.get(id=form['course_name_search'])
				else:
					if Course.objects.filter(name=form['course_name']).first():
						context['status'] = 400
						context['message'] = "Ya existe un curso con ese mismo nombre"
						context['debug'] = 1
						
					else:
						course = Course(name=form['course_name'])
						course.description = form['description']
						course.save()

						categories = form['categories'].split(',')
						for cat_id in categories:
							course.categories.add(Category.objects.get(id=cat_id))

						course.save()
						course.reload()

				if not 'teacher_register_checkbox' in form:
					teacher = Teacher.objects.get(id=form['teacher_name_search'])
				else:
					dni = form['identification_number']
					email = form['email']

					if Teacher.objects.filter(identification_number=dni).first():
						context['status'] = 400
						context['message'] = "Ya existe un profesor registrado con el mismo numero de identificacion"
						context['debug'] = {}
						context['debug']['identification_number']

					if Teacher.objects.filter(email=email).first():
						context['status'] = 400
						context['message'] = "Ya existe un profesor registrado con el mismo correo electrónico"
						context['debug'] = {}

				context['status'] = 201
				context['message'] = "Se ha realizado la apertura de un curso de manera exitosa"

			else:
				context['status'] = 400
				context['message'] = "Los datos ingresados no son validos"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)

