from django.contrib import admin
from django.urls import path
from pacientes.views import dashboard_view, lista_pacientes_view, cadastrar_paciente_view, agenda_view, detalhes_paciente_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'),
    path('pacientes/', lista_pacientes_view, name='lista_pacientes'),
    path('novo_paciente/', cadastrar_paciente_view, name='novo_paciente'),
    path('agenda/', agenda_view, name='agenda_view'),
    path('pacientes/<int:paciente_id>/', detalhes_paciente_view, name='detalhes_paciente'),
]
