from datetime import datetime
from json import dumps, loads
from uuid import uuid4

from django.db import models
from django.utils import timezone


class Attendance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	enrollment = models.ForeignKey('courses.Enrollment', on_delete=models.CASCADE)
	date = models.DateField(default=timezone.now)

	def __str__(self):
		return "Asistencia({student}, {course}, {date})".format(
			student=self.enrollment.student.full_name(),
			course=self.enrollment.opening.course.name,
			date=str(self.date)
		)

	def to_json(self, *args, **kwargs):
		as_json = loads(super().to_json(*args, **kwargs))
		as_json['id'] = str(self.id)
		as_json['enrollment'] = loads(enrollment.to_json())
		as_json['date'] = str(self.date)

		return dumps(as_json)