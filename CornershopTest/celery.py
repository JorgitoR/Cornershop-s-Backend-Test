from __future__ import absolute_import
from django.conf import settings
from celery import Celery
import os

#Nos permite correr administrativamente las tares como manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CornershopTest.settings")

#Celery app
func = Celery("CornershopTest")

#configuracion
func.config_from_object('django.conf:settings', namespace='CELERY')

#Busqueda de toda las tareas en el proyecto
func.autodiscover_tasks()