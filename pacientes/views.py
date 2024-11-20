from django.shortcuts import render, redirect, get_object_or_404
from pacientes.models import Paciente, Agendamento
from pacientes.forms import PacienteForm
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import AgendamentoForm
import datetime
import json


def home_view(request):
    if request.method == 'GET':
        return render(request, 'home.html')





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

def criar_agendamento_view(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            # Validar conflitos de horário
            paciente = form.cleaned_data['paciente']
            data = form.cleaned_data['data']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fim = form.cleaned_data['hora_fim']

            conflitos = Agendamento.objects.filter(
                paciente=paciente,
                data=data,
                hora_inicio__lt=hora_fim,
                hora_fim__gt=hora_inicio
            )

            if conflitos.exists():
                form.add_error(None, "Já existe um agendamento para este paciente nesse horário.")
            else:
                form.save()
                return redirect('agenda')  # Redireciona para a agenda
    else:
        form = AgendamentoForm()

    return render(request, 'criar_agendamento.html', {'form': form})

def cadastrar_paciente_view(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()  # Inicializa o formulário para GET ou outros métodos

    return render(request, 'cadastrar_paciente.html', {'form': form})

def detalhes_paciente_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    return render(request, 'detalhes_paciente.html', {'paciente': paciente})


def lista_pacientes_view(request):
    pacientes = Paciente.objects.all()
    return render(request, 'lista_pacientes.html', {'pacientes': pacientes})


def agenda_view(request):
    agendamentos = Agendamento.objects.all()
    eventos = []
    for agendamento in agendamentos:
        eventos.append({
            'title': agendamento.paciente.nome,
            'start': agendamento.inicio_completo.isoformat(),
            'end': agendamento.fim_completo.isoformat(),
            'description': agendamento.descricao,
        })
    return render(request, 'agenda.html', {'eventos': eventos})


def criar_agendamento_view(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            # Validar conflitos de horário
            paciente = form.cleaned_data['paciente']
            data = form.cleaned_data['data']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fim = form.cleaned_data['hora_fim']

            conflitos = Agendamento.objects.filter(
                paciente=paciente,
                data=data,
                hora_inicio__lt=hora_fim,
                hora_fim__gt=hora_inicio
            )

            if conflitos.exists():
                form.add_error(None, "Já existe um agendamento para este paciente nesse horário.")
            else:
                form.save()
                return redirect('agenda_view')  # Redireciona para a agenda
    else:
        form = AgendamentoForm()

    return render(request, 'criar_agendamento.html', {'form': form})


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