from json import dumps, loads
from uuid import uuid4

from django.db import models

from ..core.models import BaseModel


class Category(BaseModel):

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	name = models.CharField(max_length=128, unique=True)

	def __str__(self):
		return "Categoria({id}, {name})".format(
			id=self.id,
			name=self.name
		)

	def to_json(self, *args, **kwargs):
		as_json = loads(super().to_json(*args, **kwargs))
		as_json['id'] = str(self.id)
		as_json['name'] = self.name

		return dumps(as_json)