from rest_framework import serializers
from main.models import *

class ComunidadSerializer(serializers.ModelSerializer):
	usuarios = serializers.SlugRelatedField(many=True, read_only=True, slug_field='nombre')

	class Meta:
		model = Comunidad
		fields = ('id','nombre','created','usuarios')

class CaravanaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Caravana
		fields = ('id','nombre','origen','destino','comunidad','ruta','fecha_salida','lider')
			
class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Usuario
		fields = ('id','user','nombre','celular','comunidad')

	def get_comunidad(self,obj):
		return obj.comunidad.nombre