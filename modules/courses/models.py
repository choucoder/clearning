from datetime import datetime
from json import dumps, loads
from uuid import uuid4

from django.db import models
from django.utils import timezone

from ..categories.models import Category
from ..core.models import BaseModel
from ..students.models import Student
from ..teachers.models import Teacher


class Course(BaseModel):

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	name = models.CharField(max_length=128, unique=True)
	categories = models.ManyToManyField(Category)
	description = models.CharField(max_length=1024)

	def __str__(self):
		return "Curso({name}, {description})".format(
			name=self.name,
			description=self.description
		)

	def to_json(self, *args, **kwargs):
		as_json = loads(super().to_json(*args, **kwargs))
		as_json['id'] = str(self.id)
		as_json['name'] = self.name
		as_json['description'] = self.description
		as_json['categories'] = []

		for category in self.categories.all():
			as_json['categories'].append(loads(category.to_json()))

		return as_json
		

class CourseOpening(BaseModel):

	ENROLLED = 1
	IN_PROGRESS = 2
	FINALIZED = 3

	STATUS_CHOICES = [
		(ENROLLED, 'INSCRITO'),
		(IN_PROGRESS, 'EN PROGRESO'),
		(FINALIZED, 'FINALIZADO'),
	]

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	price = models.FloatField(default=20)

	start_date = models.DateField(default=timezone.now)
	end_date = models.DateField()
	students = models.ManyToManyField(Student, through='Enrollment')

	status = models.PositiveSmallIntegerField(default=STATUS_CHOICES[0][0],
											  choices=STATUS_CHOICES)

	def __str__(self):
		return "InscripcionCurso({course} {teacher}, {start} - {end} {status})".format(
			course=self.course.name,
			teacher=self.teacher.full_name(),
			start=self.start_date,
			end=self.end_date,
			status=self.get_status_display()
		)


	def to_json(self, *args, **kwargs):
		as_json = loads(super().to_json(*args, **kwargs))
		as_json['id'] = str(self.id)
		as_json['course'] = loads(self.course.to_json())
		as_json['teacher'] = loads(self.teacher.to_json())
		as_json['price'] = self.price
		as_json['start_date'] = str(self.start_date)
		as_json['end_date'] = str(self.end_date)
		as_json['status'] = self.status
		as_json['status_display'] = self.get_status_display()
		as_json['students'] = []

		students = self.students.all()

		for student in students:
			as_json['students'].append(student.to_json())

		return dumps(as_json)


class Enrollment(BaseModel):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	opening = models.ForeignKey(CourseOpening, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)

	def __str__(self):
		return "EstudianteInscrito(Estudiante '{student_name} en {course_name}' en el periodo {start_date} - {end_date}".format(
			id=self.id,
			course_name=self.opening.course.name,
			student_name=self.student.full_name(),
			start_date=str(self.opening.start_date),
			end_date=str(self.opening.end_date),
		)

	def to_json(self):
		as_json = loads(super().to_json())
		as_json['id'] = str(self.id)
		as_json['opening'] = loads(self.opening.to_json())
		as_json['student'] = loads(self.student.to_json())
		as_json['notes'] = []

		notes = ExamNote.objects.filter(enrollment=self)

		for note in notes:
			as_json['notes'].append(loads(note.to_json()))

		return dumps(as_json)


class EnrollmentPayment(BaseModel):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
	amount = models.FloatField()

	def __str__(self):
		return "PagoCurso({amount}$ {student})".format(
			id=self.id,
			amount=self.amount
		)

	def to_json(self, *args, **kwargs):
		as_json = loads(super().to_json(*args, **kwargs))
		as_json['id'] = str(self.id)
		as_json['enrollment'] = loads(self.enrollment.to_json())
		as_json['amount'] = self.amount

		return dumps(as_json)


class ExamNote(BaseModel):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
	note = models.FloatField(default=0)

	def __str__(self):
		return "NotaDeExamen({note}pts, {student}, {course}, {start} - {end})".format(
			note=self.note,
			student=self.enrollment.student.full_name(),
			course=self.enrollment.opening.course.name,
			start=str(self.enrollment.opening.start_date),
			end=str(self.enrollment.opening.end_date)
		)

	def to_json(self):
		as_json = loads(super().to_json())
		as_json['id'] = str(self.id)
		as_json['note'] = self.note
		as_json['enrollment'] = loads(self.enrollment.to_json())

		return dumps(as_json)