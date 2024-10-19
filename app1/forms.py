# app1/forms.py

from django import forms
from .models import SolicitudCambio, Proyecto

class SolicitudCambioForm(forms.ModelForm):
    class Meta:
        model = SolicitudCambio
        fields = ['solicitud']
        widgets = {
            'solicitud': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe los cambios que deseas realizar...'
            }),
        }

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['cliente', 'nombre', 'tipo', 'descripcion', 'requerimientos', 'fecha_inicio', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'requerimientos': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
