from django.contrib import admin
from main.models import *

# Register your models here.


class ComunidadAdmin(admin.ModelAdmin):
	list_display = ['nombre','created','last_modified']

	class Meta:
		model = Comunidad
		ordering = ['created']

class UsuarioAdmin(admin.ModelAdmin):
	list_display = ['user','nombre','celular','comunidad','created','last_modified']

	class Meta:
		model = Usuario
		ordering = ['created']

class VanAdmin(admin.ModelAdmin):
	list_display = ['placa','marca','color','num_cupos','created','last_modified']

	class Meta:
		model = Van
		ordering = ['created']

class ConductorVanAdmin(admin.ModelAdmin):
	list_display = ['cedula','celular','nombre','van','user','created','last_modified']

	class Meta:
		model = ConductorVan
		ordering = ['created']

class LiderCaravanaAdmin(admin.ModelAdmin):
	list_display = ['nombre','celular','created','last_modified']

	class Meta:
		model = LiderCaravana
		ordering = ['created']

class SuscripcionAdmin(admin.ModelAdmin):
	list_display = ['usuario','lugar_subida','comentarios','esta_pago','created','last_modified']

	class Meta:
		model = Suscripcion
		ordering = ['created']

class CaravanaAdmin(admin.ModelAdmin):
	list_display = ['nombre','origen','destino','ruta','fecha_salida','lider','comunidad','created','last_modified']

	class Meta:
		model = Caravana
		ordering = ['created']

class PublicacionCarroAdmin(admin.ModelAdmin):
	list_display = ['conductor','origen','destino','num_cupos','ruta','fecha_publicacion','costo','fecha_salida','created','last_modified']

	class Meta:
		model = PublicacionCarro
		ordering = ['created']

class PublicacionCaravanaAdmin(admin.ModelAdmin):
	list_display = ['lider','origen','destino','ruta','fecha_publicacion','fecha_salida','created','last_modified']

	class Meta:
		model = PublicacionCaravana
		ordering = ['created']

class RutaVanAdmin(admin.ModelAdmin):
	list_display = ['origen','destino','ruta','nombre','costo','comunidad','created','last_modified']

	class Meta:
		model = RutaVan
		ordering = ['created']

class ServicioVanAdmin(admin.ModelAdmin):
	list_display = ['van','hora_origen','hora_destino','descripcion','ruta_van','created','last_modified']

	class Meta:
		model = ServicioVan
		ordering = ['created']

admin.site.register(Comunidad, ComunidadAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Van, VanAdmin)
admin.site.register(ConductorVan, ConductorVanAdmin)
admin.site.register(LiderCaravana, LiderCaravanaAdmin)
admin.site.register(Suscripcion, SuscripcionAdmin)
admin.site.register(Caravana, CaravanaAdmin)
admin.site.register(PublicacionCarro, PublicacionCarroAdmin)
admin.site.register(RutaVan, RutaVanAdmin)
admin.site.register(ServicioVan, ServicioVanAdmin)
admin.site.register(PublicacionCaravana,PublicacionCaravanaAdmin)

