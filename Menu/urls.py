from django.urls import path

from .views import ( 
					MenuLista, 
					DetailMenu,
					CrearMenu, 
					ActualizarMenu,
					add_opciones, 
					menu_hoy)


urlpatterns = [
	
	path('', MenuLista.as_view(), name='menu'),
	path('menu/detail/<uuid:menu_id>/', DetailMenu.as_view(), name='detail'),
	path('crear_menu/', CrearMenu.as_view(), name='crear_menu'),
	path('actualizar_menu/<uuid:menu_id>/', ActualizarMenu.as_view(), name='actualizar_menu'),
	path('menu/<uuid:menu_id>/crear/opciones/', add_opciones, name='crear_opciones'),
	path('menu/<uuid:menu_id>/actualizar/opciones/', add_opciones, name='actualizar_opciones'),
	path('menu/<uuid:menuuid_id>/', menu_hoy, name='menu_hoy'),

]