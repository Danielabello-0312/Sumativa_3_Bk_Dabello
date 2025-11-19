from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    rut = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '12.345.678-9'
        })
    )
    
    class Meta:
        model = Reserva
        fields = ['rut']