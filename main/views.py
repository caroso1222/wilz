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
		return PublicacionCaravana.objects.filter(lider=usuario)

class CaravanasDeUsuario(generics.ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	serializer_class = CaravanaSerializer

	def get_queryset(self):
		usuario = Usuario.objects.get(user = self.request.user)
		return Caravana.objects.filter(suscripciones__usuario=usuario).distinct()

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
	

