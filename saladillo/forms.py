


from django import forms
from ckeditor.fields import RichTextFormField
from .models import CuerpoMail, PedidoParaMail


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
    
class FormCuerpoMail(forms.ModelForm):
    class Meta:
        model = CuerpoMail
        fields = ('body_uno', 'body_dos', 'body_tres', 'body_cuatro','body_cinco','body_seis','body_siete','body_ocho','body_nueve','body_diez','body_once','body_doce','body_trece','body_catorce')
    
    
# class FormCuerpoMail(forms.Form):
    
#     instancia = forms.IntegerField()
#     body_uno = RichTextFormField()
#     body_dos = RichTextFormField()
#     body_tres = RichTextFormField()
#     body_cuatro = RichTextFormField()
#     body_cinco = RichTextFormField()
#     body_seis = RichTextFormField()
#     body_siete = RichTextFormField()
#     body_ocho = RichTextFormField()
#     body_nueve = RichTextFormField()
#     body_diez = RichTextFormField()
#     body_once = RichTextFormField()
#     body_doce = RichTextFormField()
#     body_trece = RichTextFormField()
#     body_catorce = RichTextFormField()