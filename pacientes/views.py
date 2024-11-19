from django.shortcuts import render, redirect, get_object_or_404
from pacientes.models import Paciente, Agendamento
from pacientes.forms import PacienteForm
from django.http import JsonResponse
import datetime
import json

def agenda_view(request):
    # Obtendo todos os agendamentos do banco de dados
    agendamentos = Agendamento.objects.all()
    
    # Convertendo os agendamentos para o formato necessário para o FullCalendar
    eventos = []
    for agendamento in agendamentos:
        eventos.append({
            'title': agendamento.titulo,  # Ou o nome do paciente, se preferir
            'start': agendamento.data_inicio.isoformat(),
            'end': agendamento.data_fim.isoformat() if agendamento.data_fim else None,
            'description': agendamento.descricao,
        })
    
    # Renderizando o template com os eventos
    return render(request, 'agenda.html', {'eventos': eventos})


def cadastrar_paciente_view(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()  # Inicializa o formulário para GET ou outros métodos

    return render(request, 'cadastrar_paciente.html', {'form': form})


def lista_pacientes_view(request):
    pacientes = Paciente.objects.all()
    return render(request, 'lista_pacientes.html', {'pacientes': pacientes})


def detalhes_paciente_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    return render(request, 'detalhes_paciente.html', {'paciente': paciente})


def calendario_view(request):
    # Assuming you are fetching Agendamento objects here
    eventos = Agendamento.objects.all()

    # Serialize the events into a JSON format
    eventos_data = [
        {
            'title': agendamento.paciente.nome,
            'start': agendamento.data_hora.isoformat(),  # Ensure the datetime is in ISO format
            'end': agendamento.data_hora.isoformat(),    # If you have an 'end' time, include it here
        }
        for agendamento in eventos
    ]
    
    eventos_json = json.dumps(eventos_data)

    return render(request, 'calendario.html', {'eventos_json': eventos_json})


def agendamentos_por_paciente(request, paciente_id):
    agendamentos = Agendamento.objects.filter(paciente_id=paciente_id)
    eventos = []
    for agendamento in agendamentos:
        eventos.append({
            'title': agendamento.paciente.nome,
            'start': agendamento.inicio_completo.isoformat(),
            'end': agendamento.fim_completo.isoformat(),
            'description': agendamento.descricao,
        })
    
    return JsonResponse(eventos, safe=False)

def dashboard_view(request):
    pacientes = Paciente.objects.all()  # Pega todos os pacientes
    return render(request, 'dashboard.html', {'pacientes': pacientes})