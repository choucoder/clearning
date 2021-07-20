from datetime import datetime
from uuid import uuid4

from django.db import models

from ..core.models import BaseModel


class Student(BaseModel):

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	identification_number = models.CharField(max_length=16, unique=True)
	names = models.CharField(max_length=64)
	surnames = models.CharField(max_length=64)
	email = models.EmailField(max_length=64, unique=True)
	phone = models.CharField(max_length=16, default="")


	def to_json(self):
		return {
			'id': str(self.id),
			'identification_number': self.identification_number,
			'names': self.names,
			'surnames': self.surnames
		}

	def __str__(self):
		return "{identification_number}, {names}, {surnames}".format(
			identification_number=self.identification_number,
			names=self.names,
			surnames=self.surnames
		)

	def asistio(self):
		now = datetime.now()
		asistencia = AsistenciaBasica.objects.filter(
			student=self, year=now.year, month=now.month, day=now.day
		).first()

		print(f"Asistencia: {asistencia}")

		if asistencia != None:
			return 'true'
		else:
			return 'false'


class AsistenciaBasica(BaseModel):

	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	year = models.IntegerField()
	month = models.IntegerField()
	day = models.IntegerField()