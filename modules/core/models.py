from json import dumps, loads
from uuid import uuid4

from django.db import models


class RestManager(models.Manager):

	def to_json(self):
		_objects = super().get_queryset().filter()
		_list = []

		for _object in _objects:
			_list.append(loads(_object.to_json()))

		return dumps(_list)


class BaseModel(models.Model):

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = RestManager()

	status_choices = [
		('A', 'ACTIVE'),
		('I', 'INACTIVE'),
	]

	status = models.CharField(
		max_length=8,
		choices=status_choices,
		default=status_choices[0][0]
	)

	def to_json(self, *args, **kwargs):
		as_json = {}
		as_json['created_at'] = str(self.created_at)
		as_json['updated_at'] = str(self.updated_at)
		as_json['status'] = self.status
		as_json['status_display'] = self.get_status_display()

		return dumps(as_json)

	class Meta:
		abstract = True


class Day(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	es_name = models.CharField(max_length=8, unique=True)
	en_name = models.CharField(max_length=8, unique=True)
	day_number = models.IntegerField(unique=True)

	objects = RestManager()

	def __str__(self):
		return "Dia({es_name}, {en_name}, {day_number})".format(
			es_name=self.es_name,
			en_name=self.en_name,
			day_number=self.day_number
		)

	def to_json(self):
		as_json = {}
		as_json['id'] = str(self.id)
		as_json['es_name'] = self.es_name
		as_json['en_name'] = self.en_name
		as_json['day_number'] = self.day_number

		return dumps(as_json)