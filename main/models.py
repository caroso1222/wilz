from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class Comunidad(models.Model):
	nombre = models.CharField(max_length=100)
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	url_email = models.CharField(max_length=100)
	last_modified = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ('created',)

class Ubicacion(models.Model):
	longitud = models.CharField(max_length = 100)
	latitud = models.CharField(max_length = 100)
	created = models.DateTimeField(auto_now_add = True, auto_now = False)

	def __unicode__(self):
		return ("%s,%s")%(self.longitud,self.latitud)

	class Meta:
		ordering = ('created',)


class Usuario(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name="usern")
	nombre = models.CharField(max_length = 100)
	celular = models.CharField(max_length = 100)
	comunidad = models.ForeignKey(Comunidad, related_name="usuarios")
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	last_modified = models.DateTimeField(auto_now = True)
	ubicacion = models.ForeignKey(Ubicacion,related_name="ubicacion",blank=True, null=True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ('created',)

class Van(models.Model):
	placa = models.CharField(max_length = 100)
	marca = models.CharField(max_length = 100)
	color = models.CharField(max_length = 100)
	num_cupos = models.IntegerField()
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	last_modified = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.placa

	class Meta:
		ordering = ('created',)

class ConductorVan(models.Model):
	cedula = models.CharField(max_length = 100)
	celular = models.CharField(max_length = 100)
	nombre = models.CharField(max_length = 100)
	van = models.ForeignKey(Van)
	user = models.OneToOneField(User)
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	last_modified = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ('created',)

class LiderCaravana(models.Model):
	nombre = models.CharField(max_length = 100)
	celular = models.CharField(max_length = 100)
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	last_modified = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ('created',)

class Suscripcion(models.Model):
	usuario = models.ForeignKey(Usuario)
	lugar_subida = models.CharField(max_length = 100)
	comentarios = models.TextField(blank = True)
	esta_pago = models.BooleanField()
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	last_modified = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.usuario.nombre

	class Meta:
		ordering = ('created',)

#Wilz Bici
class Caravana(models.Model):
	nombre = models.CharField(max_length = 100)
	origen = models.CharField(max_length = 100)
	destino = models.CharField(max_length = 100)
	ruta = models.CharField(max_length = 100)
	fecha_salida = models.DateTimeField()
	lider = models.OneToOneField(LiderCaravana)
	suscripciones = models.ManyToManyField(Suscripcion, blank = True)
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	comunidad = models.ForeignKey(Comunidad)
	last_modified = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ('created',)

class PublicacionCaravana(models.Model):
	lider = models.ForeignKey(Usuario)
	origen = models.CharField(max_length = 100)
	destino = models.CharField(max_length = 100)
	ruta = models.TextField()
	fecha_publicacion = models.DateTimeField(auto_now_add = True, auto_now = False)
	fecha_salida = models.DateTimeField()
	suscripciones = models.ManyToManyField(Suscripcion, blank = True)
	empezo = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	last_modified = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return "%s. %s - %s" %(self.lider.nombre,self.origen,self.destino)

	class Meta:
		ordering = ('created',)

#Wilz Carro
class PublicacionCarro(models.Model):
	conductor = models.ForeignKey(Usuario)
	origen = models.CharField(max_length = 100)
	destino = models.CharField(max_length = 100)
	num_cupos = models.IntegerField()
	ruta = models.TextField()
	fecha_publicacion = models.DateTimeField(auto_now_add = True, auto_now = False)
	costo = models.IntegerField()
	fecha_salida = models.DateTimeField()
	suscripciones = models.ManyToManyField(Suscripcion)
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	last_modified = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return "%s. %s - %s" %(self.conductor.nombre,self.origen,self.destino)

	class Meta:
		ordering = ('created',)

#Wilz Van
class RutaVan(models.Model):
	origen = models.CharField(max_length = 100)
	destino = models.CharField(max_length = 100)
	ruta = models.TextField()
	nombre = models.CharField(max_length = 100)
	costo = models.IntegerField()
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	comunidad = models.ForeignKey(Comunidad)
	last_modified = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ('created',)

class ServicioVan(models.Model):
	van = models.ForeignKey(Van)
	hora_origen = models.TimeField()
	hora_destino = models.TimeField()
	descripcion = models.TextField()
	suscripciones = models.ManyToManyField(Suscripcion)
	ruta_van = models.ForeignKey(RutaVan)
	created = models.DateTimeField(auto_now_add = True, auto_now = False)
	last_modified = models.DateTimeField(auto_now = True)

	def __unicode__(self):
		return "%s - %s" %(self.ruta_van.nombre, self.van.placa)

	class Meta:
		ordering = ('created',)

