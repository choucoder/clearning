from uuid import uuid4

from django.db import models

from ..core.models import BaseModel
from users.models import UserAccount


class Teacher(BaseModel):

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	identification_number = models.CharField(max_length=16, unique=True)
	names = models.CharField(max_length=32)
	surnames = models.CharField(max_length=32)
	email = models.EmailField()
	phone = models.CharField(max_length=16, default="")

	account = models.ForeignKey(UserAccount, models.SET_NULL, blank=True, null=True) 

	def __str__(self):
		return "{identification_number}, {names}, {surnames}".format(
			identification_number=self.identification_number,
			names=self.names,
			surnames=self.surnames
		)

	def to_json(self):
		as_dict = {}
		as_dict['id'] = str(self.id)
		as_dict['identification_number'] = self.identification_number
		as_dict['names'] = self.names
		as_dict['surnames'] = self.surnames
		if self.account:
			as_dict['account'] = self.account.to_json()

		return as_dict

	def full_name(self):
		first_name = self.names.split()[0]
		first_surname = self.surnames.split()[0]

		return "{name} {surname}".format(
			name=first_name,
			surname=first_surname
		)

	def send_email_for_set_password(self):
		pass