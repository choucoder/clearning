from uuid import uuid4

from django.contrib.auth.models import AbstractUser, User
from django.db import models

from modules.core.models import BaseModel
from modules.plans.models import Plan


class UserAccount(AbstractUser):
	
	ADMIN = 1
	SUBSCRIPTION = 2
	TEACHER	= 3
	STUDENT = 4

	USER_TYPE_CHOICES = [
		(ADMIN, 'ADMINISTRADOR'),
		(SUBSCRIPTION, 'SUBSCRIPTION'),
		(TEACHER, 'PROFESOR'),
		(STUDENT, 'ALUMNO'),
	]

	user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,
												 default=USER_TYPE_CHOICES[1][0])

	verified = models.BooleanField(default=False)
	subscriptions = models.ManyToManyField(Plan, through='AccountSubscriptions')


	def __str__(self):
		return "{nombre}, {apellido} [{tipo}]".format(
			nombre=self.first_name,
			apellido=self.last_name,
			tipo=self.get_user_type_display()
		)

	@property
	def full_name(self):
		return f"{self.first_name} {self.last_name}"


	def to_json(self, subscriptions=False):
		as_dict = {}
		as_dict['id'] = str(self.id)
		as_dict['first_name'] = self.first_name
		as_dict['last_name'] = self.last_name
		as_dict['user_type'] = self.user_type
		as_dict['user_type_display'] = self.get_user_type_display()
		as_dict['verified'] = self.verified

		if subscriptions:
			as_dict['subscriptions'] = []

			for s in self.subscriptions.all():
				as_dict['subscriptions'].append(s.to_json())

		return as_dict


class AccountSubscriptions(BaseModel):

	status_choices = [
		('A', 'ACTIVE'),
		('I', 'INACTIVE'),
	]

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

	status = models.CharField(
		max_length=8,
		choices=status_choices,
		default=status_choices[0][0]
	)

	def __str__(self):
		return "{_id}, {account}, {plan}".format(
			_id=self.id,
			account=str(self.account),
			plan=str(self.plan)
		)