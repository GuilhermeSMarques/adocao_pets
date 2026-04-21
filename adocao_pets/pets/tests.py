from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Pet, SolicitacaoAdocao


class PetPermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='usuario',
            password='SenhaTeste123',
        )
        self.staff = User.objects.create_user(
            username='admin',
            password='SenhaTeste123',
            is_staff=True,
        )
        self.pet = Pet.objects.create(
            nome='Luna',
            idade=2,
            porte=Pet.PORTE_PEQUENO,
            especie=Pet.ESPECIE_GATO,
            raca='SRD',
            descricao='Pet disponivel para adocao.',
            status=Pet.STATUS_DISPONIVEL,
        )

    def test_usuario_comum_nao_acessa_crud_administrativo(self):
        self.client.login(username='usuario', password='SenhaTeste123')

        urls = [
            reverse('pets:pet_create'),
            reverse('pets:pet_update', args=[self.pet.pk]),
            reverse('pets:pet_delete', args=[self.pet.pk]),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, reverse('pets:pet_list'))

    def test_staff_acessa_crud_administrativo(self):
        self.client.login(username='admin', password='SenhaTeste123')

        response = self.client.get(reverse('pets:pet_create'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('pets:pet_update', args=[self.pet.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('pets:pet_delete', args=[self.pet.pk]))
        self.assertEqual(response.status_code, 200)

    def test_usuario_comum_nao_ve_pet_indisponivel_de_outro_usuario(self):
        self.pet.status = Pet.STATUS_EM_PROCESSO
        self.pet.save(update_fields=['status'])

        self.client.login(username='usuario', password='SenhaTeste123')
        response = self.client.get(reverse('pets:pet_detail', args=[self.pet.pk]))

        self.assertEqual(response.status_code, 404)


class SolicitacaoPermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='usuario',
            password='SenhaTeste123',
        )
        self.staff = User.objects.create_user(
            username='admin',
            password='SenhaTeste123',
            is_staff=True,
        )
        self.pet = Pet.objects.create(
            nome='Thor',
            idade=3,
            porte=Pet.PORTE_MEDIO,
            especie=Pet.ESPECIE_CACHORRO,
            raca='SRD',
            descricao='Pet para teste de solicitacao.',
            status=Pet.STATUS_DISPONIVEL,
        )

    def test_usuario_comum_cria_solicitacao_e_pet_fica_em_processo(self):
        self.client.login(username='usuario', password='SenhaTeste123')

        response = self.client.post(
            reverse('pets:criar_solicitacao', args=[self.pet.pk]),
            {'mensagem': 'Gostaria de adotar este pet.'},
        )

        self.assertRedirects(response, reverse('pets:minhas_solicitacoes'))
        self.assertTrue(
            SolicitacaoAdocao.objects.filter(usuario=self.user, pet=self.pet).exists(),
        )

        self.pet.refresh_from_db()
        self.assertEqual(self.pet.status, Pet.STATUS_EM_PROCESSO)

    def test_usuario_nao_cria_solicitacao_duplicada(self):
        SolicitacaoAdocao.objects.create(
            usuario=self.user,
            pet=self.pet,
            mensagem='Primeira solicitacao.',
        )

        self.client.login(username='usuario', password='SenhaTeste123')
        response = self.client.post(
            reverse('pets:criar_solicitacao', args=[self.pet.pk]),
            {'mensagem': 'Segunda solicitacao.'},
        )

        self.assertRedirects(response, reverse('pets:minhas_solicitacoes'))
        self.assertEqual(
            SolicitacaoAdocao.objects.filter(usuario=self.user, pet=self.pet).count(),
            1,
        )

    def test_staff_nao_cria_solicitacao(self):
        self.client.login(username='admin', password='SenhaTeste123')

        response = self.client.post(
            reverse('pets:criar_solicitacao', args=[self.pet.pk]),
            {'mensagem': 'Admin tentando solicitar.'},
        )

        self.assertRedirects(response, reverse('pets:pet_detail', args=[self.pet.pk]))
        self.assertFalse(
            SolicitacaoAdocao.objects.filter(usuario=self.staff, pet=self.pet).exists(),
        )

    def test_usuario_comum_nao_acessa_telas_administrativas_de_solicitacao(self):
        solicitacao = SolicitacaoAdocao.objects.create(
            usuario=self.user,
            pet=self.pet,
            mensagem='Solicitacao para teste.',
        )

        self.client.login(username='usuario', password='SenhaTeste123')

        response = self.client.get(reverse('pets:listar_solicitacoes'))
        self.assertRedirects(response, reverse('pets:pet_list'))

        response = self.client.get(
            reverse('pets:atualizar_status_solicitacao', args=[solicitacao.pk]),
        )
        self.assertRedirects(response, reverse('pets:pet_list'))

    def test_staff_aprova_solicitacao_e_pet_fica_adotado(self):
        solicitacao = SolicitacaoAdocao.objects.create(
            usuario=self.user,
            pet=self.pet,
            mensagem='Solicitacao para teste.',
        )

        self.client.login(username='admin', password='SenhaTeste123')
        response = self.client.post(
            reverse('pets:atualizar_status_solicitacao', args=[solicitacao.pk]),
            {'status': SolicitacaoAdocao.STATUS_APROVADA},
        )

        self.assertRedirects(response, reverse('pets:listar_solicitacoes'))

        solicitacao.refresh_from_db()
        self.pet.refresh_from_db()
        self.assertEqual(solicitacao.status, SolicitacaoAdocao.STATUS_APROVADA)
        self.assertEqual(self.pet.status, Pet.STATUS_ADOTADO)

    def test_staff_e_redirecionado_da_lista_de_solicitacoes_proprias(self):
        self.client.login(username='admin', password='SenhaTeste123')

        response = self.client.get(reverse('pets:minhas_solicitacoes'))

        self.assertRedirects(response, reverse('pets:listar_solicitacoes'))
