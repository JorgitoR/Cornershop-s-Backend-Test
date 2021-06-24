from django import forms

from .models import Menu, Ordenar

class MenuForm(forms.ModelForm):
	class Meta:
		model = Menu
		fields = [
			"titulo",
			"creado",
			"enviar"
		]



class OrdenarForm(forms.ModelForm):
	class Meta:
		model = Ordenar
		fields = '__all__'
		exclude = ['empleado', 'menu']

