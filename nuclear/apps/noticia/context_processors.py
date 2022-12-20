from .models import Persona
from .views import validarUsr

def isAdmin(request):
    return {'tipouser' : validarUsr(request)}