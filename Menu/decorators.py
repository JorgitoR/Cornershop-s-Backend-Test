from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def chef_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
	"""	
	Decorador de vistas que comprueba que el usuario que ha iniciado sesión es un chef,
    redirige a la página de inicio de sesión si es necesario.
	"""
	actual_decorator = user_passes_test(

        lambda u: u.is_active and u.chef,
        login_url=login_url,
        redirect_field_name=redirect_field_name

	)
	if function:
		return actual_decorator(function)
	return actual_decorator

def empleado_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
	"""
		Decorador de vistas que comprueba que el usuario que ha iniciado sesión es un empleado,
     	redirige a la página de inicio de sesión si es necesario.
	"""
	actual_decorator = user_passes_test(

		lambda u: u.is_active and u.empleado,
		login_url=login_url,
		redirect_field_name=redirect_field_name

	)
	if function:
		return actual_decorator(function)
	return actual_decorator