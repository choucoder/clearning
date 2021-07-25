from datetime import datetime
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
		return "{name}, {description}".format(
			name=self.name,
			description=self.description
		)

	def to_json(self):
		course_as_dict = {}
		course_as_dict['id'] = str(self.id)
		course_as_dict['name'] = self.name
		course_as_dict['description'] = self.description
		course_as_dict['categories'] = []

		for category in self.categories.all():
			course_as_dict['categories'].append(category.to_json())

		return course_as_dict
		

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
		return "{course} {teacher}, {start} - {end} {status}".format(
			course=self.course.name,
			teacher=self.teacher.full_name(),
			start=self.start_date,
			end=self.end_date,
			status=self.get_status_display()
		)


	def to_json(self):
		as_dict = {}
		as_dict['id'] = str(self.id)
		as_dict['course'] = self.course.to_json()
		as_dict['teacher'] = self.teacher.to_json()
		as_dict['start_date'] = str(self.start_date)
		as_dict['end_date'] = str(self.end_date)
		as_dict['status'] = self.get_status_display()

		return as_dict


class Enrollment(BaseModel):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	opening = models.ForeignKey(CourseOpening, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)

	def __str__(self):
		return "{id} - Estudiante '{student_name}' inscrito en curso '{course_name}' en el periodo {start_date} - {end_date}".format(
			id=self.id,
			course_name=self.opening.course.name,
			student_name=self.student.full_name(),
			start_date=str(self.opening.start_date),
			end_date=str(self.opening.end_date),
		)


class EnrollmentPayment(BaseModel):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
	amount = models.FloatField()

	def __str__(self):
		return "{id} {amount}".format(
			id=self.id,
			amount=self.amount
		)