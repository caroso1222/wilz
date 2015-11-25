# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from main.models import *
from main.serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import json
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.generic import View
from rest_framework.response import Response
from rest_framework import generics
from django.core.mail import send_mail
import sys

class ComunidadViewSet(viewsets.ModelViewSet):
	print >> sys.stderr, "string or object goes here"

	authentication_classes = ()
	permission_classes = (AllowAny,)

	#def get_queryset(self):
		#print self.request.META
	#	print >> sys.stderr, self.request.META
	queryset = Comunidad.objects.all()

	serializer_class = ComunidadSerializer

class UsuarioView(generics.ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	serializer_class = UsuarioSerializer

	def get_queryset(self):
		return Usuario.objects.filter(user=self.request.user)

class CaravanaView(generics.ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	serializer_class = CaravanaSerializer
	#queryset = Caravana.objects.all()
	def get_queryset(self):
		usuario = Usuario.objects.get(user = self.request.user)
		comunidad = usuario.comunidad
		return Caravana.objects.filter(comunidad=comunidad)

class PublicacionCaravanaView(generics.ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	serializer_class = PublicacionCaravanaSerializer
	#queryset = Caravana.objects.all()
	def get_queryset(self):
		usuario = Usuario.objects.get(user = self.request.user)
		comunidad = usuario.comunidad
		return PublicacionCaravana.objects.filter(lider__comunidad=comunidad).exclude(lider=usuario).order_by('fecha_salida')

class RutasView(generics.ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	serializer_class = RutasSerializer
	#queryset = Caravana.objects.all()
	def get_queryset(self):
		usuario = Usuario.objects.get(user = self.request.user)
		comunidad = usuario.comunidad
		return RutaVan.objects.filter(comunidad=comunidad)

class CaravanasLiderUsuario(generics.ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	serializer_class = PublicacionCaravanaSerializer

	def get_queryset(self):
		usuario = Usuario.objects.get(user = self.request.user)
		print usuario
		return PublicacionCaravana.objects.filter(lider=usuario)

class CaravanasDeUsuario(generics.ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	serializer_class = CaravanaSerializer

	def get_queryset(self):
		usuario = Usuario.objects.get(user = self.request.user)
		return Caravana.objects.filter(suscripciones__usuario=usuario).distinct()

class PublicacionesCaravanasDeUsuario(generics.ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	serializer_class = PublicacionCaravanaSerializer

	def get_queryset(self):
		usuario = Usuario.objects.get(user = self.request.user)
		return PublicacionCaravana.objects.filter(suscripciones__usuario=usuario).distinct()

class UsuarioACaravanaView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self,request):
		caravana = Caravana.objects.get(id=request.data["id_caravana"])
		usuario = Usuario.objects.get(user = request.user)
		direccion = request.data["direccion"]
		comentarios = request.data["comentarios"]
		suscripcion = Suscripcion(usuario=usuario,
			lugar_subida = direccion,
			comentarios = comentarios,
			esta_pago = True,
			)
		suscripcion.save()
		caravana.suscripciones.add(suscripcion)
		caravana.save()
		content = {
			'mensaje':'suscripcion exitosa',
		}
		return Response(content)


class UsuarioAPublicacionCaravanaView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	#Suscribe un usuario a una caravana de otro usuario
	def post(self,request):
		publicacionCaravana = PublicacionCaravana.objects.get(id=request.data["id_caravana"])
		usuario = Usuario.objects.get(user = request.user)
		direccion = request.data["direccion"]
		comentarios = request.data["comentarios"]
		suscripcion = Suscripcion(usuario=usuario,
			lugar_subida = direccion,
			comentarios = comentarios,
			esta_pago = True,
			)
		suscripcion.save()
		publicacionCaravana.suscripciones.add(suscripcion)
		publicacionCaravana.save()
		content = {
			'mensaje':'suscripcion exitosa',
		}
		#Envia los correos de notificacion
		nombre_lider = publicacionCaravana.lider.nombre
		email_lider = publicacionCaravana.lider.user.email
		celular_lider = publicacionCaravana.lider.celular
		nombre_usuario = usuario.nombre
		email_usuario = usuario.user.email
		celular_usuario = usuario.celular
		origen_destino = "%s - %s"%(publicacionCaravana.origen,publicacionCaravana.destino)
		send_mail('Suscripcion exitosa', 'Te has suscrito exitosamente a la caravana de %s. Puedes contactarlo en la direccion de mail %s o al numero de celular %s.'%(nombre_lider,email_lider,celular_lider), 'wilznotifications@wilz.co',   [usuario.user.email], fail_silently=False)
		send_mail('Nueva suscripcion en tu caravana', '%s se ha suscrito en tu caravana %s. Puedes contactar a %s en la direccion de mail %s o al numero de celular %s.'%(nombre_usuario,origen_destino,nombre_usuario, email_usuario, celular_usuario), 'wilznotifications@wilz.co',   [publicacionCaravana.lider.user.email], fail_silently=False)
		return Response(content)

class AnularSuscripcionAPublicacionCaravanaView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	#Elimina la suscripcion de usuario a una caravana
	def post(self,request):
		usuario = Usuario.objects.get(user = request.user)
		publicacionCaravana = PublicacionCaravana.objects.get(id=request.data["id_caravana"])
		suscripcion = publicacionCaravana.suscripciones.get(usuario=usuario)
		publicacionCaravana.suscripciones.remove(suscripcion)
		publicacionCaravana.save()
		suscripcion.delete()
		content = {
		'mensaje': 'Eliminado exitosamente'
		}
		nombre_lider = publicacionCaravana.lider.nombre
		nombre_usuario = usuario.nombre
		origen_destino = "%s - %s"%(publicacionCaravana.origen,publicacionCaravana.destino)
		send_mail('Suscripcion anulada exitosamente', 'Has anulado exitosamente tu suscripcion a la caravana de %s.'%(nombre_lider), 'wilznotifications@wilz.co',   [usuario.user.email], fail_silently=False)
		send_mail('Suscripcion anulada en tu caravana', '%s ha anulado su suscripcion a tu caravana %s.'%(nombre_usuario,origen_destino), 'wilznotifications@wilz.co',   [publicacionCaravana.lider.user.email], fail_silently=False)
		return Response(content)

@csrf_exempt
def postLocation2(request):
	print request.POST
	return HttpResponse("<p>holaaass</p>")

class EmpezarPublicacionCaravana(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self,request):
		publicacionCaravana = PublicacionCaravana.objects.get(id=request.data["id_caravana"])
		print publicacionCaravana.id
		publicacionCaravana.empezo = True
		publicacionCaravana.save()
		content = {
		'mensaje': 'Publicacion exitosa'
		}
		return Response(content)

class TerminarPublicacionCaravana(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self,request):
		publicacionCaravana = PublicacionCaravana.objects.get(id=request.data["id_caravana"])
		publicacionCaravana.empezo = False
		publicacionCaravana.save()
		content = {
		'mensaje': 'Publicacion exitosa'
		}
		return Response(content)

class PostLocation(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self,request):
		usuario = Usuario.objects.get(user = request.user)
		ubicacion = Ubicacion(longitud=request.data["location"]["longitude"],
			latitud=request.data["location"]["latitude"])
		ubicacion.save()
		usuario.ubicacion = ubicacion
		usuario.save()
		content = {
		'mensaje': 'Publicacion exitosa'
		}
		return Response(content)

class GetLocation(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self,request):
		publicacionCaravana = PublicacionCaravana.objects.get(id=request.data["id_caravana"])
		lider = publicacionCaravana.lider
		longitud = lider.ubicacion.longitud
		latitud = lider.ubicacion.latitud
		content = {
			'longitud':longitud,
			'latitud':latitud
		}
		return Response(content)

class GetLocation2(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self,request):
		lider = Usuario.objects.get(user = request.user)
		longitud = lider.ubicacion.longitud
		latitud = lider.ubicacion.latitud
		content = {
			'longitud':longitud,
			'latitud':latitud
		}
		return Response(content)

class PublicarCaravana(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self,request):
		usuario = Usuario.objects.get(user = request.user)
		origen = request.data["origen"]
		destino = request.data["destino"]
		ruta = request.data["ruta"]
		fecha_salida = request.data["fecha_salida"]
		publicacionCaravana = PublicacionCaravana(lider = usuario,
			origen = origen,
			destino = destino,
			ruta = ruta,
			fecha_salida = fecha_salida,
			)
		publicacionCaravana.save()
		content = {
		'mensaje': 'Publicacion exitosa'
		}
		return Response(content)

class RegistrarUsuario(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self,request):
		print request.data
		user_sistema = request.user
		email = request.data["email"]
		comunidad = Comunidad.objects.get(url_email = email.split("@")[1])
		nuevoUsuario = Usuario(
			user = user_sistema,
			nombre = request.data["nombre"],
			celular = request.data["celular"],
			comunidad = comunidad
			)
		nuevoUsuario.save()
		content = {
			'mensaje':'suscripcion de usuario exitosa',
		}
		return Response(content)


class ComunidadFromUser(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	#def get(self, request, format=None):
	#	content = {
	#		'user': unicode(request.user),  # `django.contrib.auth.User` instance.
	#		'auth': unicode(request.auth),  # None
	#	}
		#return Response(content)

	def get(self,request):
		usuario = Usuario.objects.get(user = request.user)
		content = {
			'user':unicode(request.user),
			'comunidad':usuario.comunidad.nombre
		}
		return Response(content)
	

