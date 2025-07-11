from django import forms
from .models import Tema, Palavra

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['nome']

class PalavraForm(forms.ModelForm):
    class Meta:
        model = Palavra
        fields = ['tema', 'texto', 'dica', 'explicacao']

class RelatorioForm(forms.Form):
    data_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Data inicial"
    )
    data_fim = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Data final"
    )
