from django.views import View
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy
from pacientes.models import Paciente, Agendamento
from pacientes.forms import PacienteForm, AgendamentoForm
from django.views.generic import ListView, CreateView


# Home View (não precisa de FormView ou outra CBV, já que só renderiza a página)
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


# Cadastrar Paciente View
class CadastrarPacienteView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'cadastrar_paciente.html'
    success_url = reverse_lazy('lista_pacientes')  # Ou qualquer URL que você deseja redirecionar após salvar

    def form_valid(self, form):
        # Aqui você pode adicionar qualquer lógica extra antes do salvar, se necessário
        return super().form_valid(form)


class ExcluirPacienteView(DeleteView):
    model = Paciente
    success_url = reverse_lazy('lista_pacientes')  # Redireciona após exclusão

    def post(self, request, *args, **kwargs):
        # Executa a exclusão via POST
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Garante que a exclusão seja feita apenas via POST
        return HttpResponseForbidden("A exclusão deve ser realizada com o método POST.")


# Detalhes Paciente View
class DetalhesPacienteView(View):
    def get(self, request, id):
        paciente = get_object_or_404(Paciente, pk=id)
        return JsonResponse({
            'nome': paciente.nome,
            'data_nascimento': paciente.data_nascimento,
            'endereco': paciente.endereco,
        })


# Editar Paciente View (usando UpdateView)
class EditarPacienteView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'editar_paciente.html'

    def get_success_url(self):
        return reverse_lazy('lista_pacientes')

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})


# Lista de Pacientes View (usando ListView)
class ListaPacientesView(ListView):
    model = Paciente
    template_name = 'lista_pacientes.html'
    context_object_name = 'pacientes'


# Agenda View (não tem muita mudança aqui, mas podemos otimizar para uma CBV)
class AgendaView(View):
    def get(self, request):
        agendamentos = Agendamento.objects.all()
        eventos = [{
            'title': agendamento.paciente.nome,
            'start': agendamento.inicio_completo.isoformat(),
            'end': agendamento.fim_completo.isoformat(),
            'description': agendamento.descricao,
        } for agendamento in agendamentos]
        return render(request, 'agenda.html', {'eventos': eventos})


class CriarAgendamentoView(FormView):
    form_class = AgendamentoForm
    template_name = 'criar_agendamento.html'
    success_url = reverse_lazy('agenda_view')

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
class AgendamentosPorPacienteView(View):
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
class DashboardView(View):
    def get(self, request):
        pacientes = Paciente.objects.all()
        return render(request, 'dashboard.html', {'pacientes': pacientes})
