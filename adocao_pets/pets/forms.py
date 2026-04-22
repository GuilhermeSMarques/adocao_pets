from django import forms

from .models import Pet, SolicitacaoAdocao


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'nome',
            'idade',
            'porte',
            'especie',
            'raca',
            'descricao',
            'status',
            'foto',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'porte': forms.Select(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-control'}),
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class SolicitacaoAdocaoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoAdocao
        fields = ['mensagem']
        widgets = {
            'mensagem': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Conte por que você quer adotar este pet.',
                },
            ),
        }


class AtualizarStatusSolicitacaoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoAdocao
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
