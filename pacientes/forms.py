from django import forms
from pacientes.models import Paciente, Agendamento
from datetime import datetime
from django.utils import formats

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'telefone', 'endereco', 'queixa_principal']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Nome completo'
            }),
            'data_nascimento': forms.DateInput(
                attrs={
                    'class': 'form-control flatpickr',
                    'type': 'text',
                    'placeholder': 'DD/MM/AAAA',
                    'data-date-format': 'd/m/Y',
                    'required': True
                }
            ),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': '(00) 00000-0000'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Endereço completo'
            }),
            'queixa_principal': forms.Textarea(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Descreva a queixa principal',
                'rows': 3
            }),
        }

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        
        if isinstance(data_nascimento, str):
            try:
                # Convert from DD/MM/YYYY to YYYY-MM-DD
                dia, mes, ano = data_nascimento.split('/')
                data_nascimento = datetime.strptime(f"{ano}-{mes}-{dia}", "%Y-%m-%d").date()
            except ValueError:
                raise forms.ValidationError("Data inválida. Use o formato DD/MM/AAAA.")

        # Validação personalizada (exemplo: impedir datas futuras)
        if data_nascimento and data_nascimento > datetime.now().date():
            raise forms.ValidationError("A data de nascimento não pode ser no futuro.")

        return data_nascimento

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.data_nascimento:
            # Convert YYYY-MM-DD to DD/MM/YYYY for display
            self.initial['data_nascimento'] = self.instance.data_nascimento.strftime('%d/%m/%Y')
        
        # Make all fields required
        for field in self.fields.values():
            field.required = True


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['paciente', 'data', 'hora_inicio', 'hora_fim', 'descricao']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'data': forms.DateInput(
                attrs={
                    'class': 'form-control flatpickr',
                    'type': 'text',
                    'placeholder': 'DD/MM/AAAA',
                    'data-date-format': 'd/m/Y',
                    'required': True
                }
            ),
            'hora_inicio': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'required': True
            }),
            'hora_fim': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'required': True
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição do agendamento'
            }),
        }

    def clean_data(self):
        data = self.cleaned_data['data']
        
        if isinstance(data, str):
            try:
                # Convert from DD/MM/YYYY to YYYY-MM-DD
                dia, mes, ano = data.split('/')
                data = datetime.strptime(f"{ano}-{mes}-{dia}", "%Y-%m-%d").date()
            except ValueError:
                raise forms.ValidationError("Data inválida. Use o formato DD/MM/AAAA.")
        
        # Validação personalizada (exemplo: impedir datas passadas)
        if data and data < datetime.now().date():
            raise forms.ValidationError("A data do agendamento não pode ser no passado.")

        return data

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')

        if hora_inicio and hora_fim and hora_inicio >= hora_fim:
            raise forms.ValidationError("A hora de início deve ser anterior à hora de término.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

