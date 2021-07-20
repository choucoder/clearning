from uuid import uuid4

from django.db import models

from ..core.models import BaseModel


class Category(BaseModel):

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	name = models.CharField(max_length=128, unique=True)

	def __str__(self):
		return "{id} {name}".format(
			id=self.id,
			name=self.name
		)

	def to_json(self):
		as_dict = {}
		as_dict['id'] = str(self.id)
		as_dict['name'] = self.name

		return as_dict