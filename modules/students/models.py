from datetime import datetime
from json import dumps, loads
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

	def to_json(self, *args, **kwargs):
		as_json = loads(super().to_json(*args, **kwargs))
		as_json['id'] = str(self.id)
		as_json['identification_number'] = self.identification_number
		as_json['names'] = self.names
		as_json['surnames'] = self.surnames
		as_json['email'] = self.email
		as_json['phone'] = self.phone

		return dumps(as_json)

	def __str__(self):
		return "Estudiante({identification_number}, {names}, {surnames})".format(
			identification_number=self.identification_number,
			names=self.names,
			surnames=self.surnames
		)

	def full_name(self):
		name = self.names.split()[0]
		surname = self.surnames.split()[0]

		return f"{name} {surname}"