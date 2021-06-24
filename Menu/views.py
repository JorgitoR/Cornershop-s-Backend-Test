from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, UpdateView, DetailView, ListView

from .models import Menu, Opcion, Ordenar
from .forms import  MenuForm, OrdenarForm
from django.forms import inlineformset_factory
from django.db import transaction

from django.db.models import Count

from datetime import datetime

from .decorators import chef_required, empleado_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



class MenuLista(ListView):
	"""
		La vista de la página principal del administrador (Nora).
	"""
	template_name = 'menu/menu.html'
	model = Menu
	context_object_name = 'menu'

	def get_queryset(self):
		if self.request.user.is_authenticated:
			qs = Menu.objects.filter(usuario=self.request.user)
			return qs 

@method_decorator([login_required, chef_required], name='dispatch')
class DetailMenu(DetailView):
	model = Menu
	queryset = Menu.objects.all()

	def get_object(self, **kwargs):
		uuid = self.kwargs['menu_id']
		return Menu.objects.get(pk=uuid)

@method_decorator([login_required, chef_required], name='dispatch')
class CrearMenu(CreateView):
	model = Menu
	form_class = MenuForm
	template_name = 'menu/crear_menu.html'

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.usuario = self.request.user
		instance.save()
		return redirect('crear_opciones', instance.pk)


@method_decorator([login_required, chef_required], name='dispatch')
class ActualizarMenu(UpdateView):
	"""
		Metodo que nos permite actualizar el Menu
	"""
	model = Menu 
	form_class = MenuForm
	context_object_name = 'menu'
	template_name = 'menu/actualizar_menu.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['opciones'] = self.get_object().opciones.annotate(opciones_count=Count('item'))
		return context

	def get_object(self, **kwargs):
		uuid = self.kwargs['menu_id']
		return Menu.objects.get(pk=uuid)

	def get_queryset(self):
		"""
			Este metodo es un gestion de permiso a nivel de objeto implicito
			Esta View solo empareja los menu de los ids de las opciones pertenecientes
			al usuario logueado
		"""
		return self.request.user.menu.all()

	def get_success_url(self):
		uuid = self.object.id
		return reverse('actualizar_menu', kwargs={'menu_id': uuid})

@login_required
@chef_required
def add_opciones(request, menu_id):
	"""
		Un metodo para agregar/actualizar las opciones del Menu
	"""
	menu = get_object_or_404(Menu, pk=menu_id)

	opcionesFormSet = inlineformset_factory(

		Menu, #Modelo Padre
		Opcion, #Modelo base
		fields = ('item',),
		min_num=2,
		validate_min=True,
		max_num=10,
		validate_max=True

	)

	if request.method == 'POST':
		form = MenuForm(request.POST, instance=menu)
		formset = opcionesFormSet(request.POST, instance=menu)
		if form.is_valid() and formset.is_valid():
			with transaction.atomic():
				form.save()
				formset.save()

			return redirect('actualizar_menu', menu.id)
	else:
		form = MenuForm(instance=menu)
		formset = opcionesFormSet(instance=menu)

	context = {
		'form':form,
		'formset':formset,

	}

	return render(request, 'menu/crear_opciones.html', context)



@login_required
@empleado_required
def menu_hoy(request, menuuid_id):
	"""
		Una vista para permitir que los empleados hagan pedidos
      	su comida preferida de hoy y personalizarla.
     	El formulario está disponible si Nora (o cualquier otro administrador)
     	ya ha llenado el menú "hoy" y si la página
     	se visita antes de las 11 AM CLT.

     	: solicitud de parámetro: la llamada del objeto de solicitud
     	: return: el menú representa el formulario HTML
	"""
	fecha = datetime.today()
	menu = get_object_or_404(Menu, pk=menuuid_id)
	opciones = Opcion.objects.filter(menu=menu)

	#Verifique si el empleado ya lo solicitó una vez al día
	instance = Ordenar.objects.filter(empleado=request.user, menu=menu)
	if instance.exists():
		titulo = '¡Estamos preparando tu comida!'
		context = {
			'titulo':titulo,
			'opciones':opciones,
			'instance':instance,
		}
		return render(request, 'menu/pedir_menu.html', context)

	#Si el empleado no Ha solicitado el menu
	if request.method == 'POST':
		opcion_menu = request.POST.get('opcion')
		opcion_id = Opcion.objects.get(id=opcion_menu)
		personalizar = request.POST.get('personalizar')

		obj = Ordenar.objects.create(
				empleado = request.user,
				menu = menu,
				opcion = opcion_id,
				personalizar =personalizar
		)

		return redirect('menu_hoy', menu.id)

	context = {
		'menu':menu,
		'opciones':opciones,
		'instance':instance,
	}

	return render(request, 'menu/pedir_menu.html', context)
