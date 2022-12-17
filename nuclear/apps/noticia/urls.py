from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns


urlpatterns = [
    # ---- Urls principales ---- #
    path('', views.NoticiaListView.as_view(), name='inicio'),
    path('<slug:slug>/', view=views.NoticiaDetailView.as_view(), name='post_detail'),
    path('categoria/<str:nombre>', views.CategoriaListView.as_view(), name='categoria'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('identidad', views.identidad, name='identidad'),
    path('vision', views.vision, name='vision'),
    path('contacto', views.contacto, name='contacto'),
    path('donaciones', views.donaciones, name='donaciones'),
    path('dashboard/index', views.dashboard, name='dashboard'),
    path('centro', views.centro, name='centro'),
    path('consultorias', views.consultorias, name='consultorias'),
    path('carpinteria', views.carpinteria, name='carpinteria'),
    path('jardineria', views.jardineria, name='jardineria'),
    path('conservas', views.conservas, name='conservas'),
    
    
    
    # ---- Urls Categorias ---- #
    path('listarCategoria', views.listarCategoria, name = 'listarCategoria'),
    path('crear-categoria', views.CrearCategoria.as_view(), name='crear-categoria'),
    path('eliminarCategoria/<int:id>', views.eliminarCategoria, name='eliminarCategoria'),
    path('editarCategoria/<int:id>', views.editarCategoria, name='editarCategoria'),
    
    # ---- Urls Noticias ---- #
    path('listarNoticias', views.listarNoticias, name = 'listarNoticias'),
    path('crear-noticia', views.CrearNoticia.as_view(), name='crear-noticia'),
    path('eliminarNoticia/<int:id>', views.eliminarNoticia, name='eliminarNoticia'),
    path('editarNoticia/<int:id>', views.editarNoticia, name='editarNoticia'),
     # ---- Urls status ---- #
    path('listarStatus', views.listarStatus, name = 'listarStatus'),
    path('crear-status', views.CrearStatus.as_view(), name='crear-status'),
    path('eliminarStatus/<int:id>', views.eliminarStatus, name='eliminarStatus'),
    path('editarStatus/<int:id>', views.editarStatus, name='editarStatus'),
    # ---- Urls Comentarios ---- #
     path('eliminarComentario/<int:id>', views.eliminarComentario, name='eliminarComentario'),
    # ---- Urls Personas ---- #
    path('crear-persona', views.CrearPersona.as_view(), name='crear-persona'),
    path('listaPersonas', views.listaPersonas, name='listaPersonas'),
    path('eliminarPersona/<int:id>', views.eliminarPersona, name='eliminarPersona'),
    path('editarPersona/<int:id>', views.editarPersona, name='editarPersona'),
    # ---- Urls Sesión ---- #
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
