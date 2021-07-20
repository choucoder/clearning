from uuid import uuid4
from django.db import models

from ..core.models import BaseModel


class Plan(BaseModel):

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=256)
	price = models.FloatField(default=0)

	def __str__(self):
		return "{name}, {description}, {price}".format(
			name=self.name,
			description=self.description,
			price=self.price
		)