from django.conf import settings
from django.db import models


class Pet(models.Model):
    PORTE_PEQUENO = 'pequeno'
    PORTE_MEDIO = 'medio'
    PORTE_GRANDE = 'grande'

    PORTE_CHOICES = [
        (PORTE_PEQUENO, 'Pequeno'),
        (PORTE_MEDIO, 'Médio'),
        (PORTE_GRANDE, 'Grande'),
    ]

    ESPECIE_CACHORRO = 'cachorro'
    ESPECIE_GATO = 'gato'

    ESPECIE_CHOICES = [
        (ESPECIE_CACHORRO, 'Cachorro'),
        (ESPECIE_GATO, 'Gato'),
    ]

    STATUS_DISPONIVEL = 'disponivel'
    STATUS_EM_PROCESSO = 'em_processo'
    STATUS_ADOTADO = 'adotado'

    STATUS_CHOICES = [
        (STATUS_DISPONIVEL, 'Disponível'),
        (STATUS_EM_PROCESSO, 'Em processo de adoção'),
        (STATUS_ADOTADO, 'Adotado'),
    ]

    nome = models.CharField(max_length=100)
    idade = models.PositiveIntegerField()
    porte = models.CharField(max_length=10, choices=PORTE_CHOICES)
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES)
    raca = models.CharField('raça', max_length=100, blank=True)
    descricao = models.TextField('descrição')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DISPONIVEL,
    )
    foto = models.ImageField(upload_to='pets/', blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_cadastro']
        verbose_name = 'pet'
        verbose_name_plural = 'pets'

    def __str__(self):
        return f'{self.nome} ({self.get_especie_display()})'


class SolicitacaoAdocao(models.Model):
    STATUS_PENDENTE = 'pendente'
    STATUS_APROVADA = 'aprovada'
    STATUS_RECUSADA = 'recusada'

    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_APROVADA, 'Aprovada'),
        (STATUS_RECUSADA, 'Recusada'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitacoes_adocao',
    )
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='solicitacoes',
    )
    mensagem = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE,
    )
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_solicitacao']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'pet'],
                name='solicitacao_unica_por_usuario_pet',
            ),
        ]
        verbose_name = 'solicitação de adoção'
        verbose_name_plural = 'solicitações de adoção'

    def __str__(self):
        return f'{self.usuario.username} - {self.pet.nome} ({self.get_status_display()})'
