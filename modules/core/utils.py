from uuid import uuid4


def get_object_or_404_json(Model, **kwargs):
	try:
		instance = Model.objects.get(**kwargs)
		return instance
	except Model.DoesNotExist:
		return JsonResponse


def get_default_uuid():
	return uuid4().hex
