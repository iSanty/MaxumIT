from django.shortcuts import render

# Create your views here.


def index_saladillo(request):
    return render(request, 'saladillo/index_saladillo.html')