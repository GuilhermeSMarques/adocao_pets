import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Cria ou atualiza um superusuario a partir de variaveis de ambiente.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'testeadmin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'vascodagama123')

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Admin nao criado: defina DJANGO_SUPERUSER_USERNAME e '
                    'DJANGO_SUPERUSER_PASSWORD no ambiente.',
                ),
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username)

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" criado.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" atualizado.'))
