from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    telefone = PhoneNumberField()
    endereco = models.CharField(max_length=200)
    queixa_principal = models.TextField()

def __str__(self):
        return self.nome


class Agendamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    descricao = models.TextField()

    def __str__(self):
        return f"Agendamento de {self.paciente.nome} em {self.data} às {self.hora_inicio}"

    @property
    def inicio_completo(self):
        return timezone.datetime.combine(self.data, self.hora_inicio)

    @property
    def fim_completo(self):
        return timezone.datetime.combine(self.data, self.hora_fim)