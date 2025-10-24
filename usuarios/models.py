# reune_app/usuarios/models.py

from django.db import models
from django.contrib.auth.models import User

# Modelo para os Cargos da empresa
class Cargo(models.Model):
    titulo = models.CharField(max_length=255, unique=True, verbose_name="Título do Cargo")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

# Modelo para as Equipes/Departamentos
class Equipe(models.Model):
    nome = models.CharField(max_length=255, unique=True, verbose_name="Nome da Equipe")
    lider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipes_lideradas', verbose_name="Líder")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    class Meta:
        verbose_name = "Equipe"
        verbose_name_plural = "Equipes"
        ordering = ['nome']

    def __str__(self):
        return self.nome

# Modelo que estende o usuário padrão do Django com informações de RH
class Colaborador(models.Model):
    # Relação 1-para-1 com o sistema de autenticação do Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Usuário")
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cargo")
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='membros', verbose_name="Equipe")
    data_admissao = models.DateField(verbose_name="Data de Admissão")
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True, verbose_name="Foto do Perfil")

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        ordering = ['usuario__first_name', 'usuario__last_name']

    def __str__(self):
        # Retorna o nome completo do usuário, ou o username se não houver nome
        return self.usuario.get_full_name() or self.usuario.username