from django import forms
from .models import *

# ---- Modelos Formularios ---- #

class NoticiaForm(forms.ModelForm):   
    class Meta:
        
        model = Noticia
        fields = ('titulo', 'subtitulo', 'contenido', 'autor', 'categoria', 'imagen', 'fechaCreacion', 'status', 'fechaPublicacion')
        autor = forms.ModelMultipleChoiceField(queryset=Persona.objects.all())
        categoria = forms.ModelMultipleChoiceField(queryset=Categoria.objects.all())
        status = forms.ModelMultipleChoiceField(queryset=Status.objects.all())
        imagen = forms.ImageField()

        
    def __init__(self, *args, **kwargs):
        super(NoticiaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
        self.fields['autor'].queryset = Persona.objects.filter(rol = 3)
        self.fields['fechaCreacion'].input_formats = ['%d/%m/%Y']
        self.fields['fechaPublicacion'].input_formats = ['%d/%m/%Y']


class CategoriaForm(forms.ModelForm):   
    class Meta:
        model = Categoria
        fields = '__all__'
        
class StatusForm(forms.ModelForm):   
    class Meta:
        model = Status
        fields = '__all__'
        
class PersonaForm(forms.ModelForm):   
    class Meta:
        model = Persona
        fields = ('username', 'nombreApellido', 'email', 'password', 'perfilImage', 'rol')
        rol = forms.ModelMultipleChoiceField(queryset=Rol.objects.all())
        perfilImage = forms.ImageField()
    
    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })