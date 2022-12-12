from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Status)
admin.site.register(Persona)
admin.site.register(Noticia)
admin.site.register(Categoria)
admin.site.register(Comentario)
admin.site.register(Rol)