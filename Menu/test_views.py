from django.test import TestCase

from .models import Menu, Opcion

class MenuViewTestCase(TestCase):

	fixtures = ["menu"]

	def test_menu_count(self):
		qs = Menu.objects.all()
		self.assertEqual(qs.count(), 3)

	def test_opcion_count(self):
		qs = Opcion.objects.all()
		self.assertEqual(qs.count(), 13)

	def test_menu_lista_view(self):
		qs = Menu.objects.all()
		response = self.client.get("/")
		self.assertEqual(response.status_code, 200)

	def test_menu_detail_view(self):
		menu = Menu.objects.all().first()
		url = menu.get_absolute_url()
		self.assertIsNotNone(url)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		context = response.context
		obj = context['object']
		self.assertEqual(obj.id, menu.id)

