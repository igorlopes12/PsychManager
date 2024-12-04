from django import forms
from pacientes.models import Paciente, Agendamento
from datetime import datetime

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'dd-mm-yyyy'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control'}),
            'queixa_principal': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')

        # Validação personalizada (exemplo: impedir datas futuras)
        if data_nascimento and data_nascimento > datetime.now().date():
            raise forms.ValidationError("A data de nascimento não pode ser no futuro.")

        return data_nascimento


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Tipo corrigido para 'date'
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_data(self):
        data = self.cleaned_data['data']  # Isso já é um objeto datetime.date

        # Validação personalizada (exemplo: impedir datas passadas)
        if data and data < datetime.now().date():
            raise forms.ValidationError("A data do agendamento não pode ser no passado.")

        return data

