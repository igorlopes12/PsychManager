from django.contrib import admin
from django.urls import path
from pacientes.views import (
    DashboardView, ListaPacientesView, CadastrarPacienteView, 
    AgendaView, DetalhesPacienteView, CriarAgendamentoView, HomeView, EditarPacienteView, ExcluirPacienteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home_view'),
    path('pacientes/', ListaPacientesView.as_view(), name='lista_pacientes'),
    path('paciente/<int:id>/detalhes/', DetalhesPacienteView.as_view(), name='detalhes_paciente'),
    path('paciente/<int:id>/editar/', EditarPacienteView.as_view(), name='editar_paciente'),
    path('paciente/<int:pk>/excluir/', ExcluirPacienteView.as_view(), name='excluir_paciente'),
    path('novo_paciente/', CadastrarPacienteView.as_view(), name='novo_paciente'),
    path('agenda/', AgendaView.as_view(), name='agenda_view'),
    path('criar-agendamento/', CriarAgendamentoView.as_view(), name='criar_agendamento'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_view'),
]

    