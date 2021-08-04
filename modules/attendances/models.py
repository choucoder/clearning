from datetime import datetime
from uuid import uuid4

from django.db import models


class Attendance(models.Model):
	id = models.StringField(primary_key=True, default=uuid4, editable=False)
	enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
	date = models.DateField(default=datetime.today().date())

	def __str__(self):

		return "Attendance({self.enrollment.student.names}"