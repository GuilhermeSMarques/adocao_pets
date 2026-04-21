from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AtualizarStatusSolicitacaoForm,
    PetForm,
    SolicitacaoAdocaoForm,
)
from .models import Pet, SolicitacaoAdocao

def home_view(request):
    pets_destaque = Pet.objects.filter(
        status=Pet.STATUS_DISPONIVEL,
    )[:4]

    total_disponiveis = Pet.objects.filter(status=Pet.STATUS_DISPONIVEL).count()

    context = {
        'pets_destaque': pets_destaque,
        'total_disponiveis': total_disponiveis,
    }
    return render(request, 'pets/home.html', context)


def staff_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('pets:pet_list')
        return view_func(request, *args, **kwargs)

    return wrapper


def pet_list_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        pets = Pet.objects.all()
    else:
        pets = Pet.objects.filter(status=Pet.STATUS_DISPONIVEL)

    return render(request, 'pets/pet_list.html', {'pets': pets})


def pet_detail_view(request, pk):
    queryset = Pet.objects.all()
    if request.user.is_authenticated and request.user.is_staff:
        pass
    elif request.user.is_authenticated:
        queryset = queryset.filter(
            Q(status=Pet.STATUS_DISPONIVEL) | Q(solicitacoes__usuario=request.user),
        ).distinct()
    else:
        queryset = queryset.filter(status=Pet.STATUS_DISPONIVEL)

    pet = get_object_or_404(queryset, pk=pk)
    return render(request, 'pets/pet_detail.html', {'pet': pet})


@staff_required
def pet_create_view(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save()
            messages.success(request, 'Pet cadastrado com sucesso.')
            return redirect('pets:pet_detail', pk=pet.pk)
    else:
        form = PetForm()

    return render(request, 'pets/pet_form.html', {'form': form})


@staff_required
def pet_update_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            pet = form.save()
            messages.success(request, 'Pet atualizado com sucesso.')
            return redirect('pets:pet_detail', pk=pet.pk)
    else:
        form = PetForm(instance=pet)

    return render(request, 'pets/pet_form.html', {'form': form, 'pet': pet})


@staff_required
def pet_delete_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if request.method == 'POST':
        pet.delete()
        messages.success(request, 'Pet excluído com sucesso.')
        return redirect('pets:pet_list')

    return render(request, 'pets/pet_confirm_delete.html', {'pet': pet})


@login_required
def criar_solicitacao_view(request, pet_pk):
    if request.user.is_staff:
        messages.error(request, 'Administradores não podem solicitar adoção.')
        return redirect('pets:pet_detail', pk=pet_pk)

    pet = get_object_or_404(Pet, pk=pet_pk)

    if SolicitacaoAdocao.objects.filter(usuario=request.user, pet=pet).exists():
        messages.info(request, 'Você já enviou uma solicitação para este pet.')
        return redirect('pets:minhas_solicitacoes')

    if pet.status != Pet.STATUS_DISPONIVEL:
        messages.error(request, 'Este pet não está disponível para novas solicitações.')
        return redirect('pets:pet_list')

    if request.method == 'POST':
        form = SolicitacaoAdocaoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.usuario = request.user
            solicitacao.pet = pet
            solicitacao.save()

            pet.status = Pet.STATUS_EM_PROCESSO
            pet.save(update_fields=['status'])

            messages.success(request, 'Solicitação de adoção enviada com sucesso.')
            return redirect('pets:minhas_solicitacoes')
    else:
        form = SolicitacaoAdocaoForm()

    return render(
        request,
        'pets/solicitacao_form.html',
        {'form': form, 'pet': pet},
    )


@login_required
def minhas_solicitacoes_view(request):
    solicitacoes = SolicitacaoAdocao.objects.filter(usuario=request.user).select_related('pet')
    return render(
        request,
        'pets/minhas_solicitacoes.html',
        {'solicitacoes': solicitacoes},
    )


@staff_required
def listar_solicitacoes_view(request):
    solicitacoes = SolicitacaoAdocao.objects.select_related('usuario', 'pet')
    return render(
        request,
        'pets/listar_solicitacoes.html',
        {'solicitacoes': solicitacoes},
    )


@staff_required
def atualizar_status_solicitacao_view(request, pk):
    solicitacao = get_object_or_404(
        SolicitacaoAdocao.objects.select_related('pet', 'usuario'),
        pk=pk,
    )

    if request.method == 'POST':
        form = AtualizarStatusSolicitacaoForm(request.POST, instance=solicitacao)
        if form.is_valid():
            solicitacao = form.save()
            pet = solicitacao.pet

            if solicitacao.status == SolicitacaoAdocao.STATUS_APROVADA:
                pet.status = Pet.STATUS_ADOTADO
            elif solicitacao.status == SolicitacaoAdocao.STATUS_RECUSADA:
                pet.status = Pet.STATUS_DISPONIVEL
            else:
                pet.status = Pet.STATUS_EM_PROCESSO

            pet.save(update_fields=['status'])
            messages.success(request, 'Status da solicitação atualizado com sucesso.')
            return redirect('pets:listar_solicitacoes')
    else:
        form = AtualizarStatusSolicitacaoForm(instance=solicitacao)

    return render(
        request,
        'pets/atualizar_status_solicitacao.html',
        {'form': form, 'solicitacao': solicitacao},
    )


@staff_required
def admin_dashboard_view(request):
    context = {
        'total_pets': Pet.objects.count(),
        'pets_disponiveis': Pet.objects.filter(status=Pet.STATUS_DISPONIVEL).count(),
        'solicitacoes_pendentes': SolicitacaoAdocao.objects.filter(
            status=SolicitacaoAdocao.STATUS_PENDENTE,
        ).count(),
    }
    return render(request, 'pets/admin_dashboard.html', context)
