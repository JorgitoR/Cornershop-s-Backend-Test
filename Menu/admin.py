from django.contrib import admin

from .models import Menu, Opcion, Ordenar, Usuario

class OpcionInline(admin.TabularInline):
	model = Opcion
	extra = 1


class MenuAdmin(admin.ModelAdmin):
	inlines = [OpcionInline,]
	class Meta:
		model = Menu 

admin.site.register(Menu, MenuAdmin)
admin.site.register(Ordenar)
admin.site.register(Usuario)
admin.site.register(Opcion)