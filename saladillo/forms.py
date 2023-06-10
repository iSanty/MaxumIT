


from django import forms
from ckeditor.fields import RichTextFormField
from .models import CuerpoMail, PedidoParaMail, Estados
from django.db import models as model
from django.contrib.auth.models import User


fields_mails = (
    ('Vacio','Vacio'),
    ('codigo_cliente','codigo_cliente'),
    ('cliente','cliente'),
    ('nro_pedido','nro_pedido'),
    ('nro_packing','nro_packing'),
    ('nro_ruteo','nro_ruteo'),
    ('mail','mail'),
    ('cantidad','cantidad'),
    ('importe_total','importe_total'),
    ('orden_de_compra','orden_de_compra'),
    
    
)

class FormActualizarPedidos(forms.Form):
    fecha = forms.DateField(input_formats=['%d/%m/%Y'])
    
    
class FormMailReceptor(forms.Form):
    mail = forms.EmailField()
    
class FormSelector(forms.Form):
    
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector1(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector2(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector3(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector4(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector5(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector6(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector7(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector8(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector9(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector10(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector11(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
class FormSelector12(forms.Form):
    selector = forms.ChoiceField(choices=fields_mails)
    
    
    
    
    
    #     'codigo_cliente',
    #     'cliente',
    #     'nro_pedido',
    #     'nro_packing',
    #     'nro_ruteo',
    #     'mail',
    #     'cantidad',
    #     'importe_total',
    #     'orden_de_compra'
    # )
    
# class FormCuerpoMail(forms.Form):
#     class Meta:
#         model = CuerpoMail
#         fields = ('body_uno', 'body_dos', 'body_tres', 'body_cuatro','body_cinco','body_seis','body_siete','body_ocho','body_nueve','body_diez','body_once','body_doce','body_trece','body_catorce')
    
    
class FormCuerpoMail(forms.Form):
    
    body_uno = RichTextFormField(required=False)
    body_dos = RichTextFormField(required=False)
    body_tres = RichTextFormField(required=False)
    body_cuatro = RichTextFormField(required=False)
    body_cinco = RichTextFormField(required=False)
    body_seis = RichTextFormField(required=False)
    body_siete = RichTextFormField(required=False)
    body_ocho = RichTextFormField(required=False)
    body_nueve = RichTextFormField(required=False)
    body_diez = RichTextFormField(required=False)
    body_once = RichTextFormField(required=False)
    body_doce = RichTextFormField(required=False)
    body_trece = RichTextFormField(required=False)
    body_catorce = RichTextFormField(required=False)
    
    
    
class FormCambiarEstado(forms.Form):
    estado = forms.ModelChoiceField(queryset=Estados.objects.all())
    
    
class FormCrearCliente(forms.Form):
    codigo = forms.IntegerField()
    nombre = forms.CharField()
    domicilio = forms.CharField()
    localidad = forms.CharField()
    cod_loc = forms.IntegerField()
    provincia = forms.CharField()
    telefono = forms.CharField()
    cuit = forms.CharField()
    cond_iva = forms.CharField()
    
    
class FormCrearPedido(forms.Form):
    codigo_cliente = forms.IntegerField()
    
    cliente = forms.CharField()
    domicilio = forms.CharField()
    localidad = forms.CharField()
    cp = forms.CharField()
    nro_pedido = forms.IntegerField()
    oc = forms.CharField()
    mail = forms.EmailField()
    
    
class FormAsignarHR(forms.Form):
    nro_hoja_de_ruta = forms.IntegerField()
    transportista = forms.ModelChoiceField(queryset=User.objects.all())
    