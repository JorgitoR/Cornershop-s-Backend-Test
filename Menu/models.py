from django.db import models

from datetime import datetime, time
from django.utils import timezone

from django.db.models.signals import post_save, pre_save

from .task import enviar_slack

from django.contrib.auth.models import AbstractUser

import uuid

class Usuario(AbstractUser):
	chef = models.BooleanField(default=False)
	empleado = models.BooleanField(default=False)


class Menu(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='menu')
	titulo = models.CharField(verbose_name='Titulo del Menu', max_length=30, default='Menu del dia')
	id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, editable=False)
	enviar = models.BooleanField(verbose_name='Enviar recordatorio a Slack', default=False)
	creado = models.DateTimeField(verbose_name='Fecha', default=datetime.now)
	actualizado = models.DateTimeField(default=timezone.now)

	class Meta:
		verbose_name ='Menu'
		verbose_name_plural='Menus'

	def __str__(self):
		return str(self.usuario.username)

	def get_absolute_url(self):
		return f"/menu/detail/{self.id}/"

	def enviado(self):
		"""
			Si el mensaje se ha enviado
		"""

		qs = True if self.enviar==True else False
		return qs 

	def elegir_menu(self):
		"""
			Elegir la comida preferida antes de las 11 AM
		"""

		fecha = datetime.now()
		ahora = time(fecha.hour, fecha.minute, fecha.second)
		print('FECHA:', fecha)
		print('FECHA:', ahora)
		qs = True if ahora.hour <= 10 and ahora.minute <= 60 else False
		print('QS', qs)
		return qs

	def actualizar(self):
		"""
			Si el menu ha sido actualizado
		"""

		fecha_creado = time(self.creado.hour, self.creado.minute, self.creado.second)
		actualizado = time(self.actualizado.hour, self.actualizado.minute, self.creado.second)

		qs = False if fecha_creado == actualizado else True
		return qs

class Opcion(models.Model):
	menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='opciones')
	item = models.CharField(max_length=120)
	creado = models.DateTimeField(auto_now_add=True)
	actualizar = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name='Opcion'
		verbose_name_plural = 'Opciones'

	def __str__(self):
		return self.item

	def update(self):
		"""
			Si la opcion del menu ha sido actualizada
		"""
		creado = time(self.creado.hour, self.creado.minute, self.creado.second)
		actualizar = time(self.actualizar.hour, self.actualizar.minute, self.actualizar.second)

		qs = False if creado == actualizar else True
		return qs 


class Ordenar(models.Model):
	empleado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='employer')
	menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='employer')
	opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE, related_name='employer')
	personalizar = models.CharField(max_length=220, null=True, blank=True)
	creado = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name='Orden del empleado'

	def __str__(self):
		return self.empleado.username


"""
	Signal para enviar al Email y Slack
"""

def post_menu(instance, *args, **kwargs):

	if instance.enviar == True:
		opcion = Opcion.objects.filter(menu__id=instance.id)
		enviar_slack(opcion, instance.id)

post_save.connect(post_menu, sender=Menu)