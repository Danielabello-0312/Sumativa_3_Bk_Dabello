from django.shortcuts import render, get_object_or_404, redirect
from .models import Sala, Reserva
from .forms import ReservaForm
from django.utils import timezone
from datetime import datetime, timedelta

def inicio(request):
    return render(request, "app_salas/inicio.html")

def salas(request):
    salas = Sala.objects.all()
    return render(request, "app_salas/salas.html", {"salas": salas})

def seleccionar_sala(request):
    salas = Sala.objects.filter(disponible=True)
    return render(request, "app_salas/seleccionar_sala.html", {"salas": salas})

def reservar(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)

    if not sala.disponible:
        return render(request, "app_salas/no_disponible.html", {"sala": sala})

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            
            fecha_str = request.POST.get('fecha')
            hora_str = request.POST.get('hora_inicio')
            duracion = int(request.POST.get('duracion_horas', 2))
            
            
            fecha_hora = datetime.strptime(f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M")
            fecha_hora = timezone.make_aware(fecha_hora)
            
            
            reserva = form.save(commit=False)
            reserva.sala = sala
            reserva.inicio = fecha_hora
            reserva.termino = fecha_hora + timedelta(hours=duracion)
            reserva.save()

        
            sala.disponible = False
            sala.save()

            return redirect("inicio")
    else:
        form = ReservaForm()

    return render(request, "app_salas/reservar.html", {"form": form, "sala": sala})

def mis_reservas(request):
    reservas_activas = Reserva.objects.filter(termino__gte=timezone.now()).order_by('inicio')
    reservas_pasadas = Reserva.objects.filter(termino__lt=timezone.now()).order_by('-termino')[:10]
    
    return render(request, "app_salas/mis_reservas.html", {
        "reservas_activas": reservas_activas,
        "reservas_pasadas": reservas_pasadas
    })

def cancelar_reserva(request, reserva_id):
    if request.method == "POST":
        reserva = get_object_or_404(Reserva, id=reserva_id)
        sala = reserva.sala
        
        sala.disponible = True
        sala.save()
        
        reserva.delete()
    
    return redirect('mis_reservas')