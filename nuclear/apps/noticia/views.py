from django.views import generic
from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import *
from .forms import *
from django.contrib import messages


    

# ----- vistas principales ----- #

def Principal(request):
    return render(request, 'base/index.html')

def plantilla(request):
    return render(request, 'plantilla/index.html')

def nosotros(request):
    return render(request, 'miscelaneo/nosotros.html')

def mision(request):
    return render(request, 'miscelaneo/mision.html')

def vision(request):
    return render(request, 'miscelaneo/vision.html')

def galeria(request):
    return render(request, 'miscelaneo/galeria.html')

def contacto(request):
    return render(request, 'miscelaneo/contacto.html')


# ----- vistas de Sesión ----- #

def login(request):
    if request.method=="POST":
        try:
            detalleUsuario=Persona.objects.get(email=request.POST['email'], password=request.POST['password'])
            print("Usuario=", detalleUsuario)
            request.session['email']=detalleUsuario.email
            if detalleUsuario.rol.id == 2:
                return render(request, 'base/dashboard.html')
            else:
                return render(request, 'base/index.html')
        except Persona.DoesNotExist as e:
            messages.success(request, 'Nombre de usuario o Contraseña incorrecto')
    return render(request, 'sesion/login.html')

def logout(request):
    try:
        del request.session['email']
    except:
        return render(request, 'base/index.html')
    return render(request, 'base/index.html')

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
            return redirect('inicio')        
    else:
        return render(request, 'sesion/register.html')
    
# -------------------------------- #
def validarUsr(request):
    x = Persona.objects.get(email = request.session['email'])
    print(x.nombreApellido)
    return x.rol.id == 2
    
# -------------------------------- #


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

def eliminarCategoria(request, id):
    if validarUsr(request):
        categoria = Categoria.objects.get(id=id)
        categoria.delete()
        return redirect('listarCategoria')
    else:
        return render(request, 'miscelaneo/error.html')

def editarCategoria(request, id):
    if validarUsr(request):
        categoria = Categoria.objects.get(id=id)
        form = CategoriaForm(request.POST or None, request.FILES or None, instance=categoria)
        if form.is_valid() and request.POST:
            form.save()
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
            return redirect('listaPersonas')
        return render(request, "persona/modificar_persona.html", {'form': form})
    else:
        return render(request, 'miscelaneo/error.html')

# ----- vistas de Comentarios ----- #

# ver como sería ....


