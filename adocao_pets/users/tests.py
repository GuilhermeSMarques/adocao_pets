from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserAuthTests(TestCase):
    def test_cadastro_cria_usuario_comum_e_autentica(self):
        response = self.client.post(
            reverse('users:register'),
            {
                'username': 'novo_usuario',
                'email': 'novo@example.com',
                'password1': 'SenhaForte123',
                'password2': 'SenhaForte123',
            },
        )

        self.assertRedirects(response, reverse('users:perfil'))

        user = User.objects.get(username='novo_usuario')
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'novo@example.com')

    def test_perfil_exige_login(self):
        response = self.client.get(reverse('users:perfil'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_login_com_credenciais_validas_redireciona_para_perfil(self):
        User.objects.create_user(
            username='usuario',
            password='SenhaTeste123',
        )

        response = self.client.post(
            reverse('users:login'),
            {
                'username': 'usuario',
                'password': 'SenhaTeste123',
            },
        )

        self.assertRedirects(response, reverse('users:perfil'))
