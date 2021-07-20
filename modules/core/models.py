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

	def to_json(self):
		as_dict = {}

		for attr, value in self.__dict__.items():
			if type(value) in (int, float, bool, str):
				as_dict[attr] = value
			elif type(value) in (BaseModel):
				as_dict[attr] = value.to_json()
			elif type(value) in (models.DateTimeField, models.DateField):
				as_dict[attr] = str(value)
			else:
				# Convert to str or None
				try:
					as_dict[attr] = str(value)
				except:
					pass

		return as_dict

	class Meta:
		abstract = True