from datetime import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from ..students.models import Student, AsistenciaBasica


class RequestConsumer(WebsocketConsumer):

	def connect(self):
		self.room_group_prefix = "rqconsumer_%s"
		self.channels = []
		self.accept()

	def disconnect(self, close_code):
		for channel in self.channels:
			async_to_sync(self.channel_layer.group_discard)(
				channel,
				self.channel_name
			)


	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		msg_type = text_data_json['msg_type']

		if msg_type == "SUBSCRIBE":
			channel_group_name = self.room_group_prefix % text_data_json['channel']
			async_to_sync(self.channel_layer.group_add) (
				channel_group_name,
				self.channel_name
			)
			self.channels.append(channel_group_name)

		else:
			reply = {}
			resource = text_data_json['resource']
			resource_action = text_data_json['action']
			form_data = text_data_json['data']

			if resource == "STUDENT":
				if resource_action == "CREATE":
					try:
						student = Student(**form_data)
						student.save()
						reply = student.to_json()
						reply['status'] = 201
					except:
						reply['status'] = 500

			if resource == "ASISTENCIA":
				if resource_action == "CREATE":
					try:
						now = datetime.now()
						student = Student.objects.filter(id=form_data['id']).first()
						asistencia = AsistenciaBasica.objects.filter(
							student=student, year=now.year, month=now.month, day=now.day
						).first()

						reply['id'] = form_data['id']
						
						if asistencia:
							if form_data['checked']:
								reply['status'] = 200
								reply['checked'] = True
							else:
								asistencia.delete()
								reply['status'] = 200
								reply['checked'] = False

						else:
							if form_data['checked']:
								asistencia = AsistenciaBasica(
									student=student,
									year=now.year,
									month=now.month,
									day=now.day
								)
								asistencia.save()
								reply['checked'] = True
								reply['status'] = 200
							else:
								reply['checked'] = False
								reply['status'] = 200

					except:
						reply['status'] = 500

			status = reply.pop('status', 404)

			for channel in self.channels:
				async_to_sync(self.channel_layer.group_send) (
					channel,
					{
						'resource': resource,
						'action': resource_action,
						'msg_type': 'REQUEST',
						'type': 'chat_message',
						'data': reply,
						'status': status
					}
				)

	def chat_message(self, event):
		msg_type = event['msg_type']
		resource = event['resource']
		resource_action = event['action']

		self.send(text_data=json.dumps({
			'msg_type': msg_type,
			'resource': resource,
			'action': resource_action,
			'data': event['data'],
			'status': event['status']
		}))
