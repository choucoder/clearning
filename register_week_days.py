import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "clearning.settings")
django.setup()

from modules.core.models import Day


days = [
	(0, 'Lunes', 'Monday'),
	(1, 'Martes', 'Thuesday'),
	(2, 'Miercoles', 'Wednesday'),
	(3, 'Jueves', 'Thursday'),
	(4, 'Viernes', 'Friday'),
	(5, 'Sabado', 'Saturday'),
	(6, 'Domingo', 'Sunday'),
]

for number, es_name, en_name in days:
	try:
		_day = Day(day_number=number, es_name=es_name, en_name=en_name)
		_day.save()
		print(f"El dia {es_name} ha sido guardado")

	except Exception as e:
		print(f"El dia {es_name} ya esta registrado -> {e}")