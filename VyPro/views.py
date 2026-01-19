from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
from .models import *

def pagina_no_encontrada(request, exception):
    return render(request, '404.html', status=404)

def error_servidor(request):
    return render(request, '500.html', status=500)

def index(request):
    listar_servicio = Servicio.objects.filter(visible=True)
    galeria = Galeria.objects.all()

    paginator = Paginator(galeria, 9)
    page_number = request.GET.get('page')
    galeria = paginator.get_page(page_number) 

    data = {
        'servicio': listar_servicio,
        'galeria': galeria
    }   

    return render(request, 'web/index.html', data)

def detalle_servicio(request, id):
    listar_servicio = Servicio.objects.filter(visible=True)
    servicio_encontrado = get_object_or_404(Servicio, id=id)
    galeria = Galeria.objects.filter(servicio=servicio_encontrado).order_by('-fecha')[:20]

    paginator = Paginator(galeria, 9)
    page_number = request.GET.get('page')
    galeria = paginator.get_page(page_number) 

    data = {
        'servicio_encontrado': servicio_encontrado,
        'servicio': listar_servicio,
        'galeria': galeria,
    }

    return render(request, 'web/detalle_servicio.html', data)

def contacto(request):
    listar_servicio = Servicio.objects.filter(visible=True)

    data = {
        'servicio': listar_servicio,
        'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY,
    }

    if request.POST:
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        empresa = request.POST.get("empresa")
        telefono = request.POST.get("telefono")
        correo = request.POST.get("correo")
        servicio = request.POST.get("servicio")
        mensaje = request.POST.get("mensaje")
        recaptcha = request.POST.get("g-recaptcha-response")
        telefono_limpio = telefono.replace(" ", "").replace("-", "") 

        if not all([nombre, apellido, empresa, telefono, correo, servicio, mensaje]):
            messages.error(request, 'Por favor, Ingrese todos los campos')
            return redirect('contacto')

        if len(nombre) < 3 or len(nombre) > 30: 
            messages.error(request, 'El campo nombre debe tener entre 3 y 30 caracteres')
            return redirect('contacto')
        
        if len(apellido) < 3 or len(apellido) > 30:
            messages.error(request, 'El campo apellido debe tener entre 3 y 30 caracteres')
            return redirect('contacto')

        if not nombre.replace(" ", "").isalpha():
            messages.error(request, 'el campo nombre no debe tener numeros o caracteres especiales')
            return redirect('contacto')
        
        if not apellido.replace(" ", "").isalpha():
            messages.error(request, 'El campo apellido no debe tener numeros o caracteres especiales')
            return redirect('contacto')

        if len(empresa) < 3 or len(empresa) > 100:
            messages.error(request, 'La empresa debe tener entre 3 y 100 caracteres')
            return redirect('contacto')  

        if not telefono_limpio.isdigit(): 
            messages.error(request, "El campo teléfono solo debe tener números")
            return redirect('contacto')

        if len(telefono_limpio) != 9: 
            messages.error(request, 'El campo teléfono debe tener 9 dígitos Ej: 9123456789')
            return redirect('contacto')

        try:
            if servicio == 'otros':
                registro_servicio = Servicio.objects.get(nombre="Otro servicio") 
            else:
                registro_servicio = Servicio.objects.get(nombre=servicio)
        except Servicio.DoesNotExist:
            messages.error(request, 'El servicio seleccionado no es válido o no existe')
            return redirect('contacto')

        data_recaptcha = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY, 
            'response': recaptcha
        }

        try:
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data_recaptcha)
            respuesta = r.json()
        except:
            messages.error(request, "Error de conexión, intente más tarde")
            return redirect('contacto')

        print("respuesta de recaptcha:", respuesta)

        if respuesta['success']:
            form = Formulario(
                nombre=nombre,
                apellido=apellido,
                empresa=empresa,
                telefono=telefono_limpio, 
                correo=correo,
                servicio=registro_servicio,
                mensaje=mensaje
            )

            try:
                form.save()
                messages.success(request, 'Formulario enviado, Nos pondremos en contacto pronto')
                return redirect('contacto')
            except Exception:
                messages.error(request, "Hubo un error al enviar el formulario. Por favor Intente nuevamente")
        else: 
            messages.error(request, 'Por favor complete el RECAPTCHA para continuar')
            
        return render(request,'web/contacto.html', data)
    return render(request, 'web/contacto.html', data)

def nosotros(request):
    listar_servicio = Servicio.objects.filter(visible=True)

    data = {
        'servicio':listar_servicio
    }

    return render(request, 'web/nosotros.html', data)




