from json import dumps, loads
from uuid import uuid4

from django.db import models

from ..core.models import BaseModel


class Plan(BaseModel):

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=256)
	price = models.FloatField(default=0)

	def __str__(self):
		return "Plan({name}, {description}, {price})".format(
			name=self.name,
			description=self.description,
			price=self.price
		)

	def to_json(self, *args, **kwargs):
		as_json = loads(super().to_json(*args, **kwargs))
		as_json['id'] = str(self.id)
		as_json['name'] = self.name
		as_json['description'] = self.description
		as_json['price'] = self.price

		return dumps(as_json)