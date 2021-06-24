from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from .models import Menu, Opcion, Ordenar

from django.contrib.auth import get_user_model

User = get_user_model()

class MenuTestCase(TestCase):

	fixtures = ["menu"]

	'''
		Configuramos nuestras Test
	'''
	def setUp(self):
		usuario = User.objects.create(username='nora')
		self.menu = Menu(pk=1)
		date = timezone.now()
		self.menu_a = Menu.objects.create(usuario=usuario, creado=date)
		self.menu_b = Menu.objects.create(usuario=usuario, creado=date)

		self.opcion_a = Opcion.objects.create(menu=self.menu_a, item='Arroz con pollo')
		self.opcion_b = Opcion.objects.create(menu=self.menu_b, item='Pezcado frito')

	def test_actualizado(self):
		get_actualizado = self.menu.actualizar()
		self.assertEquals(get_actualizado, True)

	def test_enviado(self):
		'''
			Test si no ha sido enviado
		'''
		get_enviado = self.menu.enviado()
		self.assertEquals(get_enviado, False)

	def test_uuid_unique(self):
		'''
			Test de nuestro uuid, debe ser unico
		'''
		self.assertNotEqual(self.menu_a.id, self.menu_b.id)

	def test_opcion_menu(self):
		'''
			Test de nuestra opcion related al menu 
		'''	
		self.assertEqual(self.opcion_a.menu, self.menu_a)
