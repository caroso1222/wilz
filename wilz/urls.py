from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from main import views
from main.views import *
from allauth.account.views import confirm_email as allauthemailconfirmation
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router2 = DefaultRouter()
router2.register(r'comunidades',views.ComunidadViewSet,base_name = "comunidad")


urlpatterns = [
    # Examples:
    # url(r'^$', 'wilz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(router2.urls)),
    url(r'^api2/caravanas/', CaravanaView.as_view()),
    url(r'^api2/publicaciones-caravanas/', PublicacionCaravanaView.as_view()),
    url(r'^api2/rutas/', RutasView.as_view()),
    url(r'^api2/caravanas-lider-usuario/', CaravanasLiderUsuario.as_view()),
    url(r'^api2/usuario/', UsuarioView.as_view()),
    url(r'^api2/registrar-usuario/', RegistrarUsuario.as_view()),
    url(r'^api2/agregar-usuario-caravana/', UsuarioACaravanaView.as_view()),
    url(r'^api2/agregar-usuario-publicacion-caravana/', UsuarioAPublicacionCaravanaView.as_view()),
    url(r'^api2/caravanas-usuario/', CaravanasDeUsuario.as_view()),
    url(r'^api2/empezar-publicacion-caravana/', EmpezarPublicacionCaravana.as_view()),
    url(r'^api2/terminar-publicacion-caravana/', EmpezarPublicacionCaravana.as_view()),
    url(r'^api2/post-location/', PostLocation.as_view()),
    url(r'^api2/get-location/', GetLocation.as_view()),
    url(r'^api2/get-location-2/', GetLocation2.as_view()),
    url(r'^api2/post-location-2/', views.postLocation2),
    url(r'^api2/publicaciones-caravanas-de-usuario/', PublicacionesCaravanasDeUsuario.as_view()),
    url(r'^api2/anular-suscripcion-a-publicacion-caravana/', AnularSuscripcionAPublicacionCaravanaView.as_view()),
    url(r'^api2/comunidad-usuario/', ComunidadFromUser.as_view()),
    url(r'^api2/publicar-caravana/', PublicarCaravana.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>\w+)/$', allauthemailconfirmation, name="account_confirm_email"),
    #url(r'^accounts/profile/$', RedirectView.as_view(url='/'), name='profile-redirect'),
]

#urlpatterns = format_suffix_patterns(urlpatterns)