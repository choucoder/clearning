import qrcode
import os
from json import dumps, loads
from uuid import uuid4

from django.db import models

from ..core.models import BaseModel
from ..core.utils import get_default_uuid
from users.models import UserAccount


class Teacher(BaseModel):

	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	identification_number = models.CharField(max_length=16, unique=True)
	qrcode = models.CharField(max_length=36, unique=True, default=get_default_uuid)
	qrcode_path = models.CharField(max_length=255, blank=True, null=True)

	names = models.CharField(max_length=32)
	surnames = models.CharField(max_length=32)
	email = models.EmailField()
	phone = models.CharField(max_length=16, default="")

	account = models.ForeignKey(UserAccount, models.SET_NULL, blank=True, null=True) 

	def __str__(self):
		return "Profesor({identification_number}, {names}, {surnames})".format(
			identification_number=self.identification_number,
			names=self.names,
			surnames=self.surnames
		)

	def save_credential(self):
		media_path = "media"
		
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=10,
			border=4,
		)
		qr.add_data(self.qrcode)
		qr.make(fit=True)

		img = qr.make_image(fill_color="black", back_color="white")

		if not os.path.exists(media_path):
			os.mkdir(media_path)

		if not os.path.exists(os.path.join("media", "images")):
			os.mkdir(os.path.join("media", "images"))

		media_path = os.path.join("media", "images")
		filename = "%s.%s" % (str(uuid4()).replace('-', ''), "png")

		img.save(os.path.join(media_path, filename))
		self.qrcode_path = filename

		self.save()


	def to_json(self, *args, **kwargs):
		as_json = loads(super().to_json(*args, **kwargs))
		as_json['id'] = str(self.id)
		as_json['identification_number'] = self.identification_number
		as_json['names'] = self.names
		as_json['surnames'] = self.surnames
		as_json['email'] = self.surnames
		as_json['phone'] = self.surnames

		if self.account:
			as_json['account'] = loads(self.account.to_json())

		return dumps(as_json)

	def full_name(self):
		first_name = self.names.split()[0]
		first_surname = self.surnames.split()[0]

		return "{name} {surname}".format(
			name=first_name,
			surname=first_surname
		)

	def send_email_for_set_password(self):
		pass