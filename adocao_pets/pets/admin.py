from django.contrib import admin

from .models import Pet, SolicitacaoAdocao


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'porte', 'status', 'data_cadastro')
    list_filter = ('especie', 'porte', 'status')
    search_fields = ('nome', 'raca', 'descricao')
    readonly_fields = ('data_cadastro',)


@admin.register(SolicitacaoAdocao)
class SolicitacaoAdocaoAdmin(admin.ModelAdmin):
    list_display = ('pet', 'usuario', 'status', 'data_solicitacao')
    list_filter = ('status', 'data_solicitacao')
    search_fields = ('pet__nome', 'usuario__username', 'mensagem')
    readonly_fields = ('data_solicitacao',)
