from json import dumps, loads

from django.db import models


class BaseModel(models.Model):

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

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