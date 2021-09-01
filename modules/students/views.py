from datetime import datetime
from json import dumps, loads

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .forms import (
	EnrollmentNoteForm, EnrollmentAttendanceForm, EnrollmentPaymentForm,
)
from .models import Student
from ..attendances.models import Attendance
from ..courses.models import (Enrollment, EnrollmentPayment, ExamNote)


class StudentsView(View):

	template_name = 'students/index.html'


	def get(self, request):
		context = {}

		try:
			students = Student.objects.all()
			context['students'] = students
			context['message'] = "Todos los estudiantes"

		except Exception as e:
			context['message'] = f"Error: {e}"

		return render(request, self.template_name, context)



class EnrollmentView(View):

	def get(self, request, enrollment_id):
		context = {}

		try:
			enrollment = Enrollment.objects.get(id=enrollment_id)
			context['status'] = 200
			context['message'] = "Detalles de inscripción de alumno"
			context['data'] = loads(enrollment.to_json())

		except ObjectDoesNotExist:
			context['status'] = 404
			context['message'] = "Inscripción de curso no existe"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)


class EnrollmentNotesView(View):

	form = EnrollmentNoteForm

	def get(self, request, enrollment_student_id):
		context = {}

		try:
			enrollment = Enrollment.objects.get(id=enrollment_student_id)
			exams = ExamNote.objects.filter(enrollment=enrollment)
			exams_as_json = []

			for exam in exams:
				exams_as_json.append(loads(exam.to_json()))

			context['status'] = 200
			context['message'] = "Detalles de inscripción de alumno"
			context['data'] = exams_as_json

		except ObjectDoesNotExist:
			context['status'] = 404
			context['message'] = "Inscripción de curso no existe"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)


	def post(self, request, enrollment_student_id):
		context = {}
		form = self.form(request.POST)
		
		try:
			print(enrollment_student_id)

			if form.is_valid():
				form = form.cleaned_data
				enrollment = Enrollment.objects.get(id=form['enrollment_id'])
				note = form['note']
				exam = ExamNote(note=note, enrollment=enrollment)
				exam.save()

				context['status'] = 201
				context['data'] = loads(exam.to_json())
				context['message'] = "Nota de examen ha sido guardada"
			else:
				context['status'] = 400
				context['message'] = "Datos invalidos"


		except ObjectDoesNotExist:
			context['status'] = 404
			context['message'] = "Inscripción de alumno no existe"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)


class EnrollmentAttendancesView(View):

	form = EnrollmentAttendanceForm

	def get(self, request, enrollment_id):
		context = {}

		try:
			enrollment = Enrollment.objects.get(id=enrollment_id)
			attendances = Attendance.objects.filter(enrollment=enrollment)
			attendances_as_json = []

			for attendance in attendances:
				attendances_as_json.append(loads(attendance.to_json()))

			context['status'] = 200
			context['message'] = "Lista de asistencias"
			context['data'] = attendances_as_json

		except ObjectDoesNotExist:
			context['status'] = 404
			context['message'] = "Inscripción de curso no existe"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)


	def post(self, request, enrollment_id):
		context = {}
		form = self.form(request.POST)
		
		try:
			enrollment = Enrollment.objects.get(id=enrollment_id)

			if form.is_valid():
				form = form.cleaned_data
				date = form['date']
				date = datetime.strptime(date, "%Y-%m-%d")

				attendance = Attendance.objects.filter(enrollment=enrollment, date=date).first()
				
				if not attendance:
					attendance = Attendance(enrollment=enrollment, date=date)
					attendance.save()
					context['status'] = 201
					context['message'] = "Asistencia marcada"
				else:
					attendance.delete()
					context['status'] = 200
					context['message'] = "Asistencia eliminada"	
				context['data'] = loads(attendance.to_json())

			else:
				context['status'] = 400
				context['message'] = "Datos invalidos"

		except ObjectDoesNotExist:
			context['status'] = 404
			context['message'] = "Inscripción de alumno no existe"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)


class EnrollmentPaymentsView(View):

	form = EnrollmentPaymentForm

	def get(self, request, enrollment_id):
		context = {}

		try:
			enrollment = Enrollment.objects.get(id=enrollment_id)
			payments = EnrollmentPayment.objects.filter(enrollment=enrollment)
			payments_as_json = []

			for payment in payments:
				payments_as_json.append(loads(payments.to_json()))

			context['status'] = 200
			context['message'] = "Pagos realizados"
			context['data'] = payments_as_json

		except ObjectDoesNotExist:
			context['status'] = 404
			context['message'] = "Inscripción de curso no existe"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)


	def post(self, request, enrollment_id):
		context = {}
		form = self.form(request.POST)
		
		try:
			enrollment = Enrollment.objects.get(id=enrollment_id)

			if form.is_valid():
				form = form.cleaned_data
				amount = form['amount']
				course_opening = enrollment.opening

				enrollment_payments = EnrollmentPayment.objects.filter(enrollment=enrollment)
				enrollment_payments_amounts = [ep.amount for ep in enrollment_payments]
				total_payment = sum(enrollment_payments_amounts)

				if (total_payment + amount) <= course_opening.price:
					payment = EnrollmentPayment(enrollement=enrollment, amount=amount)
					payment.save()

					context['status'] = 201
					context['message'] = "El pago se ha procesado con exito"
					context['data'] = loads(payment.to_json())
				else:
					context['status'] = 400
					context['message'] = "El pago no pudo ser procesado porque el total pagado excederia el precio del curso"
			else:
				context['status'] = 400
				context['message'] = "Datos invalidos"

		except ObjectDoesNotExist:
			context['status'] = 404
			context['message'] = "Inscripción de alumno no existe"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor: {e}"

		return JsonResponse(context)