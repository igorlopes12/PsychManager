from django.views import View
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy
from pacientes.models import Paciente, Agendamento
from pacientes.forms import PacienteForm, AgendamentoForm
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime, date


# Home View (now requires login)
class HomeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        # Get today's date
        today = date.today()
        
        # Get all events for today
        today_events = Agendamento.objects.filter(data=today).order_by('hora_inicio')
        
        # Format events for display
        events = [{
            'paciente': agendamento.paciente.nome,
            'hora_inicio': agendamento.hora_inicio.strftime('%H:%M'),
            'hora_fim': agendamento.hora_fim.strftime('%H:%M'),
            'descricao': agendamento.descricao,
            'id': agendamento.id
        } for agendamento in today_events]

        context = {
            'today_events': events,
            'user': request.user,
            'today': today.strftime('%d/%m/%Y')
        }
        return render(request, 'home.html', context)


# Cadastrar Paciente View
class CadastrarPacienteView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'cadastrar_paciente.html'
    success_url = reverse_lazy('lista_pacientes')
    login_url = 'login'

    def form_valid(self, form):
        # Aqui você pode adicionar qualquer lógica extra antes do salvar, se necessário
        return super().form_valid(form)


class ExcluirPacienteView(LoginRequiredMixin, DeleteView):
    model = Paciente
    success_url = reverse_lazy('lista_pacientes')  # Redireciona após exclusão
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        # Executa a exclusão via POST
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Garante que a exclusão seja feita apenas via POST
        return HttpResponseForbidden("A exclusão deve ser realizada com o método POST.")


# Detalhes Paciente View
class DetalhesPacienteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, id):
        paciente = get_object_or_404(Paciente, pk=id)
        return JsonResponse({
            'nome': paciente.nome,
            'data_nascimento': paciente.data_nascimento,
            'endereco': paciente.endereco,
        })


# Editar Paciente View (usando UpdateView)
class EditarPacienteView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'editar_paciente.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('lista_pacientes')

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})


# Lista de Pacientes View (usando ListView)
class ListaPacientesView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'lista_pacientes.html'
    context_object_name = 'pacientes'
    login_url = 'login'


# Agenda View (não tem muita mudança aqui, mas podemos otimizar para uma CBV)
class AgendaView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        agendamentos = Agendamento.objects.all()
        eventos = [{
            'title': agendamento.paciente.nome,
            'start': agendamento.inicio_completo.isoformat(),
            'end': agendamento.fim_completo.isoformat(),
            'description': agendamento.descricao,
        } for agendamento in agendamentos]
        return render(request, 'agenda.html', {'eventos': eventos})


class CriarAgendamentoView(LoginRequiredMixin, FormView):
    form_class = AgendamentoForm
    template_name = 'criar_agendamento.html'
    success_url = reverse_lazy('agenda_view')
    login_url = 'login'

    def form_valid(self, form):
        # Obtenha os dados diretamente do `form.cleaned_data`
        paciente = form.cleaned_data['paciente']
        data = form.cleaned_data['data']  # Este é um objeto datetime.date
        hora_inicio = form.cleaned_data['hora_inicio']
        hora_fim = form.cleaned_data['hora_fim']

        # Verifique conflitos sem alterar o tipo do campo `data`
        conflitos = Agendamento.objects.filter(
            paciente=paciente,
            data=data,
            hora_inicio__lt=hora_fim,
            hora_fim__gt=hora_inicio
        )

        if conflitos.exists():
            form.add_error(None, "Já existe um agendamento para este paciente nesse horário.")
            return self.form_invalid(form)
        
        # Salve o formulário normalmente
        form.save()
        return super().form_valid(form)


# Agendamentos por Paciente (agora usando JsonResponse, mas com lógica CBV)
class AgendamentosPorPacienteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, paciente_id):
        agendamentos = Agendamento.objects.filter(paciente_id=paciente_id)
        eventos = [{
            'title': agendamento.paciente.nome,
            'start': agendamento.inicio_completo.isoformat(),
            'end': agendamento.fim_completo.isoformat(),
            'description': agendamento.descricao,
        } for agendamento in agendamentos]
        return JsonResponse(eventos, safe=False)


# Dashboard View (similar à lista de pacientes, pode ser uma ListView também)
class DashboardView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        pacientes = Paciente.objects.all()
        return render(request, 'dashboard.html', {'pacientes': pacientes})
