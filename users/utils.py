from django.contrib.auth.hashes import make_password
from uuid import uuid4


def random_password_generate():
	password = str(uuid4()).replace('-', '')[: 10]
	return make_password(password)