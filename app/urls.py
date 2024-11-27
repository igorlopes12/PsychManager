from django.contrib import admin
from django.urls import path
from pacientes.views import (
    dashboard_view, lista_pacientes_view, CadastrarPacienteView, 
    agenda_view, detalhes_paciente_view, criar_agendamento_view, HomeView, editar_paciente_view, excluir_paciente_view
)

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('admin/', admin.site.urls),
    path('pacientes/', lista_pacientes_view, name='lista_pacientes'),
    path('paciente/<int:id>/detalhes/', detalhes_paciente_view, name='detalhes_paciente'),
    path('paciente/<int:id>/editar/', editar_paciente_view, name='editar_paciente'),
    path('paciente/excluir/<int:paciente_id>/',excluir_paciente_view, name='excluir_paciente'),
    path('novo_paciente/', CadastrarPacienteView.as_view(), name='novo_paciente'),
    path('agenda/', agenda_view, name='agenda_view'),
    path('criar-agendamento/', criar_agendamento_view, name='criar_agendamento'),
]
