from django.db import models
from django.contrib.auth.models import User

class Tema(models.Model):
    nome = models.CharField(max_length=100)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="temas_criados")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Palavra(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name="palavras")
    texto = models.CharField(max_length=100)
    dica = models.TextField(blank=True, null=True)
    explicacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.texto

class Partida(models.Model):
    palavra = models.ForeignKey(Palavra, on_delete=models.CASCADE)
    aluno = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    acertou = models.BooleanField(default=False)
    tentativas = models.PositiveIntegerField(default=0)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno or 'Anônimo'} - {self.palavra} ({'Acertou' if self.acertou else 'Errou'})"
