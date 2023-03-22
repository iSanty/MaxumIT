


from django import forms


class FormActualizarPedidos(forms.Form):
    fecha = forms.DateField(input_formats=['%d/%m/%Y'])
    
    
class FormMailReceptor(forms.Form):
    mail = forms.EmailField()