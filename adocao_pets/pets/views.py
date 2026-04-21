from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PetForm
from .models import Pet

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
    if not (request.user.is_authenticated and request.user.is_staff):
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
