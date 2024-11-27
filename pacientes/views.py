from django.views import View
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from pacientes.models import Paciente, Agendamento
from pacientes.forms import PacienteForm, AgendamentoForm
import json


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class CadastrarPacienteView(FormView):
    template_name = 'cadastrar_paciente.html'
    form_class = PacienteForm
    success_url = '/pacientes/'

    def get(self, request):
        form = PacienteForm()
        return render(request, 'cadastrar_paciente.html', {'NovoPacienteForm': form})

    def post(self, request):
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
        return render(request, 'cadastrar_paciente.html', {'NovoPacienteForm': form})


# def cadastrar_paciente_view(request):
#     if request.method == 'POST':
#         form = PacienteForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('lista_pacientes')
#     else:
#         form = PacienteForm()  # Inicializa o formulário para GET ou outros métodos

#     return render(request, 'cadastrar_paciente.html', {'NovoPacienteForm': form})


def excluir_paciente_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    paciente.delete()
    return redirect('lista_pacientes')


def detalhes_paciente_view(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    return JsonResponse({
        'nome': paciente.nome,
        'data_nascimento': paciente.data_nascimento,
        'endereco': paciente.endereco,
    })


def editar_paciente_view(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            # Em vez de redirecionar, retornar um JSON
            return JsonResponse({'success': True, 'nome': paciente.nome, 'id': paciente.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'editar_paciente.html', {'form': form, 'paciente': paciente})


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

    return render(request, 'criar_agendamento.html', {'AgendamentoForm': form})


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