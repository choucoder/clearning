from datetime import datetime
from random import randint
from pprint import pprint
import traceback

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .forms import CourseCreateForm, CourseOpeningForm, EnrollmentForm
from .models import Course, CourseOpening
from modules.categories.models import Category
from modules.students.models import Student
from modules.teachers.models import Teacher
from users.models import UserAccount
from users.utils import random_password_generate


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


class CourseOpeningView(View):

	form = CourseOpeningForm

	def post(self, request):
		context = {}

		try:
			form = self.form(request.POST)

			if form.is_valid():
				form = form.cleaned_data
				course, teacher = None, None

				date_start = form['date_start']
				date_end = form['date_end']

				date_start = datetime.strptime(date_start, "%Y-%m-%d")
				date_end = datetime.strptime(date_end, "%Y-%m-%d")

				if not date_start < date_end:
					context['status'] = 400
					context['message'] = "La fecha de inicio debe ser menor que la fecha de finalizacion"
					context['debug'] = 1
					return JsonResponse(context)

				if form['course_register_checkbox'] != 'on':
					course = Course.objects.get(id=form['course_name_search'])
				else:
					if Course.objects.filter(name=form['course_name']).first():
						context['status'] = 400
						context['message'] = "El curso que intentas registrar ya existe"
						context['debug'] = 1
						
					else:
						course = Course(name=form['course_name'])
						course.description = form['course_description']
						course.save()

						categories = form['categories'].split(',')
						for cat_id in categories:
							category = Category.objects.filter(id=cat_id).first()

							if category:
								course.categories.add(category)

						course.save()
						course.reload()

				if form['teacher_register_checkbox'] != 'on':
					teacher = Teacher.objects.get(id=form['teacher_name_search'])
				else:
					dni = form['teacher_identification_number']
					email = form['teacher_email']

					if Teacher.objects.filter(identification_number=dni).first():
						context['status'] = 400
						context['message'] = "Ya existe un profesor registrado con el mismo numero de identificacion"
						context['debug'] = 2

					elif Teacher.objects.filter(email=email).first():
						context['status'] = 400
						context['message'] = "Ya existe un profesor registrado con el mismo correo electrónico"
						context['debug'] = 2

					else:
						teacher = Teacher()
						teacher.identification_number = dni
						teacher.email = email
						teacher.names = form['teacher_names']
						teacher.surnames = form['teacher_surnames']
						teacher.phone = form['teacher_phone']
						teacher.save()
						# teacher.reload()

						users = UserAccount.objects.filter(email=email)
						email = email if not users else None

						username = f'T{teacher.identification_number}{randint(10, 99)}'
						
						try:
							user = UserAccount(
								email=email,
								first_name=teacher.names,
								last_name=teacher.surnames,
								username=username,
								password=random_password_generate(),
							)
							user.user_type = UserAccount.TEACHER
							user.save()
							
							teacher.account = user
							teacher.save() 

						except Exception as e:
							print(f"Error al crear el usuario para el profesor: {e}")

				if course and teacher:
					opening = CourseOpening()
					opening.course = course
					opening.teacher = teacher
					opening.price = form['course_price']
					opening.start_date = date_start
					opening.end_date = date_end
					opening.save()
					# opening.reload()

					context['status'] = 201
					context['message'] = "Se ha realizado la apertura de un curso de manera exitosa"
					context['data'] = opening.to_json()
			else:
				context['status'] = 400
				context['message'] = "Faltan datos. Reviselos e intentelo de nuevo"
				context['debug'] = 1

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"
			traceback.print_exc()

		return JsonResponse(context)


class CourseStudentsView(View):
	template_name = 'courses/students.html'
	form = EnrollmentForm

	def get(self, request, enrollment_id):
		context = {}
		try:
			course_enrollment = CourseOpening.objects.get(id=enrollment_id)
			enrolled_students = course_enrollment.students.all()

			unenrolled_students = []

			for student in Student.objects.all():
				if student not in enrolled_students:
					unenrolled_students.append(student)

			context['status'] = 200
			context['data'] = enrolled_students
			context['course'] = course_enrollment
			context['students'] = unenrolled_students
			context['enrollment_id'] = enrollment_id
			context['message'] = f"Estudiantes inscritos en el curso"
			template_name = self.template_name

		except ObjectDoesNotExist:
			context['status'] = 404
			template_name = 'errors/404.html'

		except Exception as e:
			traceback.print_exc()
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"
			template_name = 'errors/500.html'

		return render(request, template_name, context)


	def post(self, request, enrollment_id):
		context = {}

		try:
			opening = CourseOpening.objects.get(id=enrollment_id)

			form = self.form(request.POST)

			if form.is_valid():
				form = form.cleaned_data
				context['status'] = 201
				context['message'] = "Se ha inscrito el alumno en el curso"
			else:
				context['status'] = 400
				context['message'] = "Datos no validos. Revise el formulario e intentelo de nuevo."

		except ObjectDoesNotExist as e:
			context['status'] = 404
			context['message'] = f"Recurso {e} no encontrado"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)