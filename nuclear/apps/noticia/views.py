from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from django.views.defaults import page_not_found
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import *
from .forms import * 



def enviarcontacto(request):
    if request.method == "POST":
        name = request.POST.get('nombre', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        correo = EmailMessage(
            'Mensaje de contacto recibido',
            f'Mensaje enviado por {name} <{email}>:\n\nAsunto: {subject}\n\nMensaje {message}',
            email,
            ['gonzaloismael.cg@gmail.com'],
            reply_to=[email],
        )
        
        try:
            correo.send()
            # mensajes que se envian a la página NO ES CORREO
            titulo = 'Confirmación de contacto'
            subtitulo = 'Contacto'
            cuerpo = "Muchas gracias por contactarte con Fundación ALA'"
            subcuerpo = 'Te responderemos pronto'
            contexto = {
                'titulo' : titulo,
                'subtitulo' : subtitulo,
                'cuerpo' : cuerpo,
                'subcuerpo' : subcuerpo,
            } 
            return render(request, 'base/secciones/email_template.html', contexto)
        except:
            # mensajes que se envian a la página NO ES CORREO
            titulo = 'Lo sentimos'
            subtitulo = 'Contacto'
            cuerpo = 'No pudimos procesar tu solicitud de contacto'
            subcuerpo = 'Solicitamos que se acerque a nuestra institución'

            contexto = {
                'titulo' : titulo,
                'subtitulo' : subtitulo,
                'cuerpo' : cuerpo,
                'subcuerpo' : subcuerpo,
            } 
            return render(request, 'base/secciones/email_template.html', contexto)    

# ----- vistas de posteos ----- #
class CategoriaListView(ListView):
    model = Noticia
    context_object_name = 'noticia'
    template_name = 'categoria/categoria.html'
    def get_context_data(self, *args, **kwargs):
         categoria = get_object_or_404(Categoria, nombre=self.kwargs.get('nombre'))
         id = categoria.id
         context = super(CategoriaListView, self).get_context_data(**kwargs)
         context['noticia'] = Noticia.objects.filter(categoria=id)
         context['categoria'] = categoria
         return context

    
class NoticiaListView(ListView):
    """Detail post."""
    model = Noticia
    context_object_name = 'noticia'
    template_name = 'base/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(NoticiaListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class NoticiaDetailView(DetailView):
    """Detail post."""
    template_name = 'noticia/detalle.html'
    model = Noticia
    context_object_name = 'noticia'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
         noticia =  get_object_or_404(Noticia, slug=self.kwargs.get('slug'))
         id = noticia.id
         context = super(NoticiaDetailView, self).get_context_data(**kwargs)
         context['noticia'] = get_object_or_404(Noticia, id=id)
         context['comentarios'] = Comentario.objects.filter(noticia=id)
         context['category'] = Categoria.objects.all()
         return context
      
    def get(self, request, *args, **kwargs):
        noticia = get_object_or_404(Noticia, slug=self.kwargs.get('slug'))
        form = CommentForm()
        comentarios = Comentario.objects.filter(noticia = noticia).order_by('-fecha')
        category = Categoria.objects.all()
        context = {
            'noticia': noticia,
            'form': form,
            'comentarios': comentarios,
            'category': category
        }
        return render(request, 'noticia/detalle.html', context) 

    def post(self, request, *args, **kwargs):
        noticia = get_object_or_404(Noticia, slug=self.kwargs.get('slug'))
        id = noticia.id
        form = CommentForm(request.POST)
        comentarios = Comentario.objects.filter(noticia = id).order_by('-fecha')
        x = get_object_or_404(Persona, email = request.session['email'])
        category = Categoria.objects.all()
    
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.autor = x
            new_comment.noticia = noticia
            messages.success(request, "comentario agregado correctamente")
            new_comment.save()

        context = {
            'noticia': noticia,
            'form': form,
            'category': category,
            'comentarios': comentarios,
        }
        return render(request, 'noticia/detalle.html', context) 
    
    
# ----- vistas principales ----- #

def nosotros(request):
    return render(request, 'miscelaneo/nosotros.html')

def identidad(request):
    return render(request, 'miscelaneo/identidad.html')

def vision(request):
    return render(request, 'miscelaneo/vision.html')

def contacto(request):
    return render(request, 'miscelaneo/contacto.html')

def donaciones(request):
    return render(request, 'miscelaneo/donaciones.html')

def centro(request):
    return render(request, 'miscelaneo/centro.html')

def consultorias(request):
    return render(request, 'miscelaneo/consultorias.html')

def carpinteria(request):
    return render(request, 'miscelaneo/carpinteria.html')

def jardineria(request):
    return render(request, 'miscelaneo/jardineria.html')

def conservas(request):
    return render(request, 'miscelaneo/conservas.html')

def perfil(request):
    user = get_object_or_404(Persona, email = request.session['email'])
    return render(request, 'base/secciones/perfil.html', {'user':user})

def editarperfil(request):
    try:
        user = get_object_or_404(Persona, email = request.session['email'])
        form = PerfilForm(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid() and request.POST:
            form.save()
            return redirect('perfil')
        return render(request, "base/secciones/editarperfil.html", {'form': form})
    except:
        return render(request, 'miscelaneo/error.html')

# ----- vistas de Sesión ----- #

def login(request):
    if request.method=="POST":
        try:
            detalleUsuario=Persona.objects.get(email=request.POST['email'], password=request.POST['password'])
            print("Usuario=", detalleUsuario)
            request.session['email']=detalleUsuario.email
            if detalleUsuario.rol == 2:
                return render(request, 'base/dashboard.html')
            else:
                return redirect('inicio')
        except Persona.DoesNotExist as e:
            messages.success(request, 'Nombre de usuario o Contraseña incorrecto')
    return render(request, 'sesion/login.html')


def logout(request):
    try:
        del request.session['email']
    except:
        return redirect('inicio')
    return redirect('inicio')

def register(request):
    if request.method == "POST":
        username=request.POST["username"]
        nombreApellido=request.POST["nombreApellido"]
        email=request.POST["email"]
        password=request.POST["password"]
        email_exists = (Persona.objects.filter(email = email))
        user_exists = (Persona.objects.filter(username = username))
        if user_exists:
            messages.success(request, 'El nombre de usuario ' + request.POST['username']+' ya existe.')
            return redirect('/register')
        elif email_exists:
            messages.success(request, 'El correo electrónico ' + request.POST['email']+' ya existe.')
            return redirect('/register')
        else:
            Persona(username=username, email=email, password=password, nombreApellido=nombreApellido).save()
            request.session['email']=email
            messages.success(request, 'Te has registrado con éxito')
            return redirect('inicio')        
    else:
        return render(request, 'sesion/register.html')

def recuperarpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        email_exists = (Persona.objects.filter(email = email))
        if email_exists:
            newpass = get_random_string(length=8)
            
            correo = EmailMessage(
                "Solicitud de cambio de contraseña | Fundación ALA'",
                f'Su nueva contraseña para ingresar al sitio es {newpass}.\n\n Podrá cambiarla luego desde su perfil.',
                email,
                ['gonzaloismael.cg@gmail.com', email],
                reply_to=[email],
            )
            
            try:
                messages.success(request, f'=> "{newpass}" <= Revise su casilla de email, le enviaremos instrucciones para recuperar su cuenta')        
                correo.send()
                
                Persona.objects.filter(email = email).update(password=newpass)
                
                print(newpass)
                return redirect('/recuperarpassword')
                
            except:
                messages.success(request, f'No hemos podido enviarle el correo de recuperación, comuniquese con el administrador del sitio')        
                return redirect('/recuperarpassword')    
        else:
            messages.success(request, 'El correo electrónico ingresado no pertenece a ninguna cuenta registrada')
            return redirect('/recuperarpassword')
    else:
        return render(request, 'cambiarContraseña/restablecer_contraseña.html')
            
# ---- Validación usuario en sesión tipo admin ---- #

def validarUsr(request):
    try:
        if request.session['email']:
            x = Persona.objects.get(email = request.session['email'])
            print(x.nombreApellido)
            return x.rol == 2
    except:
        return False
    
# ============================================================================================ #
# ----------------------------------    VISTAS DASHBOARD    ----------------------------------
# ============================================================================================ #


def dashboard(request):
    if validarUsr(request):
        return render(request, 'base/dashboard.html')
    else:
        return render(request, 'miscelaneo/error.html')

# ----- vistas de categorías ----- #

def listarCategoria(request):
    if validarUsr(request):
        categorias = Categoria.objects.all()
        return render(request, "categoria/listar_categoria.html", {'categorias': categorias})
    else:
        return render(request, 'miscelaneo/error.html')

class CrearCategoria(generic.CreateView):
    model = Categoria
    template_name = 'categoria/crear_categoria.html'
    form_class = CategoriaForm
    
    def get_success_url(self):
        return reverse('listarCategoria')
    
    def post(self, request, *args, **kwargs):
        form = CategoriaForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            messages.success(request, 'Categoria creada con éxito')
            new_comment.save()
            categorias = Categoria.objects.all()
            return render(request, 'categoria/listar_categoria.html', {'categorias': categorias})
        else:
            return redirect('crear-categoria')
    
    

def eliminarCategoria(request, id):
    if validarUsr(request):
        categoria = Categoria.objects.get(id=id)
        categoria.delete()
        messages.success(request, 'Eliminado correctamente')
        return redirect('listarCategoria')
    else:
        return render(request, 'miscelaneo/error.html')

def editarCategoria(request, id):
    if validarUsr(request):
        categoria = Categoria.objects.get(id=id)
        form = CategoriaForm(request.POST or None, request.FILES or None, instance=categoria)
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, 'Categoría modificada con éxito')
            return redirect('listarCategoria')
        return render(request, "categoria/modificar_categoria.html", {'form': form})
    else:
        return render(request, 'miscelaneo/error.html')

# ----- vistas de noticias ----- #

def listarNoticias(request):
    if validarUsr(request):
        noticias = Noticia.objects.all().order_by('-fechaPublicacion')
        return render(request, "noticia/listar_noticias.html", {'noticias': noticias})
    else:
        return render(request, 'miscelaneo/error.html')

class CrearNoticia(generic.CreateView):
    model = Noticia
    template_name = 'noticia/crear_noticia.html'
    form_class = NoticiaForm

    def get_success_url(self):
        return reverse('listarNoticias')
    
    def post(self, request, *args, **kwargs):
        form = NoticiaForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            messages.success(request, 'Noticia creada con éxito')
            new_comment.save()
            noticias = Noticia.objects.all().order_by('-fechaPublicacion')
            return render(request, 'noticia/listar_noticias.html', {'noticias': noticias})
        else:
            return redirect('listarNoticias')

def eliminarNoticia(request, id):
    if validarUsr(request):
        noticia = Noticia.objects.get(id=id)
        noticia.delete()
        return redirect('listarNoticias')
    else:
        return render(request, 'miscelaneo/error.html')

def editarNoticia(request, id):
    if validarUsr(request):
        noticia = Noticia.objects.get(id=id)
        form = NoticiaForm(request.POST or None, request.FILES or None, instance=noticia)
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, 'Noticia modificada con éxito')
            return redirect('listarNoticias')
        return render(request, "noticia/modificar_noticia.html", {'form': form})
    else:
        return render(request, 'miscelaneo/error.html')

# ----- vistas de Status ----- #

def listarStatus(request):
    if validarUsr(request):
        status = Status.objects.all()
        return render(request, "status/listar_status.html", {'status': status})
    else:
        return render(request, 'miscelaneo/error.html')

class CrearStatus(generic.CreateView):
    model = Status
    template_name = 'status/crear_status.html'
    form_class = StatusForm

    def get_success_url(self):
        return reverse('listarStatus')
    
    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            messages.success(request, 'Estado creado con éxito')
            new_comment.save()
            status = Status.objects.all()
            return render(request, 'status/listar_status.html', {'status': status})
        else:
            return redirect('listarNoticias')

def eliminarStatus(request, id):
    if validarUsr(request):
        status = Status.objects.get(id=id)
        status.delete()
        return redirect('listarStatus')
    else:
        return render(request, 'miscelaneo/error.html')

def editarStatus(request, id):
    if validarUsr(request):
        status = Status.objects.get(id=id)
        form = StatusForm(request.POST or None, request.FILES or None, instance=status)
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, 'Estado modificado con éxito')
            return redirect('listarStatus')
        return render(request, "status/modificar_status.html", {'form': form})
    else:
        return render(request, 'miscelaneo/error.html')

# ----- vistas de Personas ----- #

def listaPersonas(request):
    if validarUsr(request):
        personas = Persona.objects.all()
        return render(request, "persona/listar_persona.html", {'personas': personas})
    else:
        return render(request, 'miscelaneo/error.html')

class CrearPersona(generic.CreateView):
    model = Persona
    template_name = 'persona/crear_persona.html'
    form_class = PersonaForm

    def get_success_url(self):
        return reverse('listaPersonas')
    
    def post(self, request, *args, **kwargs):
        form = PersonaForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            messages.success(request, 'Persona creada con éxito')
            new_comment.save()
            personas = Persona.objects.all()
            return render(request, 'persona/listar_persona.html', {'personas': personas})
        else:
            return redirect('listarNoticias')
  
def eliminarPersona(request, id):
    if validarUsr(request):
        persona = Persona.objects.get(id=id)
        persona.delete()
        return redirect('listaPersonas')
    else:
        return render(request, 'miscelaneo/error.html')

def editarPersona(request, id):
    if validarUsr(request):
        persona = Persona.objects.get(id=id)
        form = PersonaForm(request.POST or None, request.FILES or None, instance=persona)
        if form.is_valid() and request.POST:
            form.save()
            messages.success(request, 'Persona modificada con éxito')
            return redirect('listaPersonas')
        return render(request, "persona/modificar_persona.html", {'form': form})
    else:
        return render(request, 'miscelaneo/error.html')

# ----- Error 404 ----- #

def handler404(request, exception, template_name="404.html"):
    response = render('base/404.html')
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
    return render(request, 'base/500.html', status=500)


# ----- Comentarios ----- #

def eliminarComentario(request, id, newsid):
    if validarUsr(request):
        noticia = get_object_or_404(Noticia, id=newsid)
        slug = noticia.slug
        comentario = Comentario.objects.get(id=id)
        comentario.delete()
        messages.success(request, 'Comentario eliminado con éxito')
        return redirect(f'/{slug}')
    else:
        return render(request, 'miscelaneo/error.html')

def eliminarComentarioDash(request, id, newsid):
    if validarUsr(request):
        comentario = Comentario.objects.get(id=id)
        comentario.delete()
        return filtrarComentarios(request, newsid)
    else:
        return render(request, 'miscelaneo/error.html')

def listarComentarios(request):
    if validarUsr(request):
        noticias = Noticia.objects.all()
        return render(request, "comentarios/listar_comentarios.html", {'noticias': noticias})
    else:
        return render(request, 'miscelaneo/error.html')   
    
def filtrarComentarios(request, news_id):
    if validarUsr(request):
        if news_id == None:
            news = Noticia.objects.first()
        else:
            news = get_object_or_404(Noticia, id=news_id)
        noticias = Noticia.objects.all()
        comentarios = Comentario.objects.filter(noticia = news).order_by('-fecha')
        contexto = {
            'noticias': noticias,
            'comentarios': comentarios,
            'actual': news,
            }
        return render(request, "comentarios/listar_comentarios.html", contexto)
    else:
        return render(request, 'miscelaneo/error.html')


