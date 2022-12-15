from django.db import models
from django.utils import timezone
from django.template import defaultfilters

# --- Modelo Roles --- #

class Rol(models.Model):
    rol = models.CharField(max_length=35, verbose_name='Nombre', null=False)
    
    def delete(self, using = None, keep_parents = False):
        super().delete()
    
    def __str__(self):
        return self.rol

# --- Modelo Persona --- #

class Persona(models.Model):
    username = models.CharField(max_length=35, verbose_name="Nombre de usuario", null=False, unique=True)
    nombreApellido = models.CharField(max_length=70, verbose_name="Nombre y Apellido", null=False)
    email = models.CharField(max_length=50, verbose_name="Correo electrónico", null=False, unique=True)
    password = models.CharField(max_length=20, verbose_name="Contraseña", null=False)
    perfilImage = models.ImageField(verbose_name='Foto de perfil', blank=True, null=True, upload_to='usuarios/', default='usuarios/default.png')
    rol = models.ForeignKey(Rol, verbose_name='Rol', on_delete=models.SET_NULL, null=True, default=1)
    
    def __str__(self):
        return self.username
    
    def delete(self, using = None, keep_parents = False):
        self.perfilImage.delete(self.perfilImage.name)
        super().delete()



# --- Modelo Categoría --- #

class Categoria(models.Model):
    nombre = models.CharField(max_length=35, verbose_name='Nombre', null=False)
    
    def delete(self, using = None, keep_parents = False):
        super().delete()
    
    def __str__(self):
        return self.nombre

# --- Modelo status --- #

class Status(models.Model):
    status = models.CharField(max_length=35, verbose_name='Nombre', null=False)
    
    def delete(self, using = None, keep_parents = False):
        super().delete()
    
    def __str__(self):
        return self.status


# --- Modelo Noticias --- #

class Noticia(models.Model):
    titulo = models.CharField(max_length=100, verbose_name='Título', null=False)
    subtitulo = models.CharField(max_length=100, verbose_name='Subtitulo', null=True, blank = True)
    fechaCreacion = models.DateField(default=timezone.now, verbose_name='Fecha de creación')
    contenido = models.TextField(verbose_name='Contenido', null=True)
    imagen = models.ImageField(verbose_name='Imagen', blank=True, null=True, upload_to='noticia/', default='noticia/default.png')
    fechaPublicacion = models.DateField(default=timezone.now, verbose_name="Fecha de Publicacion")
    autor = models.ForeignKey(Persona, verbose_name='Autor', on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Categoria, verbose_name='Categoría', on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, verbose_name='Estado', on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=100, editable=False, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.titulo)
        super(Noticia, self).save(*args, **kwargs)
    
    def delete(self, using = None, keep_parents = False):
        self.imagen.delete(self.imagen.name)
        super().delete()
    
    def __str__(self):
        return self.titulo  
    
    class Meta:
        ordering = ('-fechaPublicacion',)

# --- Modelo Comentarios --- #

class Comentario(models.Model):
    
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha', null=False)
    contenido = models.CharField(max_length=50, verbose_name='Contenido', null=False)
    autor = models.ForeignKey(Persona, verbose_name='Usuario', on_delete=models.SET_NULL, null=True)
    noticia = models.ForeignKey(Noticia, verbose_name='Noticia', on_delete=models.SET, null=True)
    
    class Meta:
        ordering = ('-fecha',)
    
    def delete(self, using = None, keep_parents = False):
        super().delete()

    def __str__(self):
        return f"comentario de {self.autor} {self.contenido}"

