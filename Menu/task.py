from django.conf import settings
from celery import shared_task
from slack import WebClient


@shared_task
def enviar_slack(opcion, uuid):
	slack_token = settings.TOKEN_SLACK
	cliente = WebClient(token=slack_token)

	opciones = []
	for opcion in opcion:
		opciones.append(str(opcion.item))


	opcion_texto = str(opciones)

	url_menu = "http://localhost:8000/menu/%s" % str(uuid)

	cliente.api_call(
		'chat.postMessage',
		json={
			'channel':'#menu',
			'text':"Estimado. \nEl menu de hoy es:" + opcion_texto + "\nurl: " + url_menu + "\nSaludos !!" 
		}
	)
