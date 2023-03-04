from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.http import require_POST






@require_POST
def primer_mail(request, *args, **kwargs):
    
    
    if request.method == 'POST':
        
        cliente = request.GET.get('cliente','')
        nro_pedido = request.GET.get('nro_pedido','')
        mail = request.GET.get('mail','')
        
        body = 'Estimados ' + cliente + """
        Su pedido nro: """ + str(nro_pedido) + ' entró en nuestra base de datos.'
        
        print('to: ' + mail + """ 
              BodyMail:  """ + body)
        
        
        
        return HttpResponse('Success')