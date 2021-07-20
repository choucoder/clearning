from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .forms import TeacherCreateForm
from .models import Teacher
from users.models import UserAccount
from users.utils import random_password_generate


class TeachersView(View):

	form = TeacherCreateForm


	def post(self, request):
		context = {}

		try:
			form = self.form(request.POST)

			if form.is_valid():
				form = form.cleaned_data
				teacher = Teacher(**form)
				teacher.save()

				# Crear cuenta de profesor
				account = UserAccount()
				account.first_name = teacher.names
				account.last_name = teacher.surnames
				account.email = teacher.email
				account.username = teacher.identification_number
				account.user_type = UserAccount.TEACHER
				account.password = random_password_generate()
				account.save()

				teacher.account = account
				teacher.save()
				teacher.reload()
				context['status'] = 201
				context['message'] = f"El profesor {teacher.full_name()} ha sido registrado exitosamente"

			else:
				context['status'] = 400
				context['message'] = "Los datos ingresados son invalidos. Compruebe e intentelo de nuevo"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)


class TeacherView(View):

	def get(self, request, teacher_id):
		context = {}
		try:
			teacher = Teacher.objects.get(id=teacher_id)
			context['status'] = 200
			context['message'] = f"Profesor {teacher.full_name()}"
			context['data'] = teacher.to_json()

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)


	def put(self, request, teacher_id):
		pass

	def patch(self, request, teacher_id):
		pass

	def delete(self, request, teacher_id):
		pass
		