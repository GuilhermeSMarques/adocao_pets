# PetAdoção

Sistema web de adoção de pets desenvolvido com Python, Django, HTML e CSS para a disciplina de Programação Web.

## Integrantes

- Nome do integrante 1: Guilherme Santos Marques
- Nome do integrante 2: Matheus Fonseca Vilella

## Descrição do Projeto

O PetAdoção é um sistema acadêmico para gerenciar pets disponíveis para adoção e solicitações feitas por usuários interessados. O projeto possui autenticação, controle de acesso por tipo de usuário e CRUD completo de pets.

O sistema foi desenvolvido sem JavaScript, usando recursos padrão do Django, templates HTML, CSS puro, banco SQLite e o modelo de usuário padrão do Django.

## Tecnologias Utilizadas

- Python
- Django
- HTML
- CSS
- SQLite
- Pillow, para upload de imagens

## Perfis de Usuário

### Usuário comum

Usuários comuns são contas com is_staff=False.

Podem:

- criar conta;
- fazer login e logout;
- visualizar pets disponíveis;
- acessar detalhes de pets disponíveis;
- enviar solicitação de adoção;
- visualizar apenas as próprias solicitações.

### Administrador / ONG

Administradores são usuários com is_staff=True.

Podem:

- fazer login;
- acessar o dashboard administrativo;
- cadastrar pets;
- editar pets;
- excluir pets;
- visualizar todos os pets;
- visualizar todas as solicitações de adoção;
- alterar o status das solicitações.

## Funcionalidades

### Autenticação

- cadastro de usuário comum;
- login;
- logout;
- página de perfil;
- navegação dinâmica de acordo com o tipo de usuário.

### Pets

- listagem de pets;
- detalhes do pet;
- cadastro de pet;
- edição de pet;
- exclusão de pet;
- upload opcional de foto;
- controle de status:
  - Disponível;
  - Em processo de adoção;
  - Adotado.

### Solicitações de Adoção

- usuário comum pode solicitar adoção de um pet disponível;
- o sistema impede solicitação duplicada do mesmo usuário para o mesmo pet;
- ao enviar uma solicitação, o pet passa para "Em processo de adoção";
- administrador pode listar todas as solicitações;
- administrador pode aprovar ou recusar solicitações;
- ao aprovar uma solicitação, o pet passa para "Adotado";
- ao recusar uma solicitação, o pet volta para "Disponível".

## Estrutura do Projeto

text
adocao_pets/
├── config/
│   ├── settings.py
│   └── urls.py
├── pets/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/pets/
├── users/
│   ├── forms.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/users/
├── static/
│   ├── css/
│   └── img/
├── templates/
│   └── base.html
├── media/
├── manage.py
├── requirements.txt
└── README.md


## Como Rodar Localmente

### 1. Acessar a pasta do projeto

powershell
cd c:\Users\exemplo\dev\adocao_pets


### 2. Ativar o ambiente virtual

powershell
.\venv\Scripts\activate


### 3. Instalar as dependências

powershell
pip install -r requirements.txt


### 4. Aplicar as migrations

powershell
python manage.py migrate


### 5. Criar um usuário administrador

powershell
python manage.py createsuperuser


O superusuário criado por esse comando terá acesso ao admin do Django. Para usar o fluxo administrativo do sistema, o usuário precisa estar com is_staff=True.

### 6. Rodar o servidor local

powershell
python manage.py runserver


Depois acesse o ip que consta no terminal.


## Manual Básico de Uso

### Visitante

1. Acesse a página inicial.
2. Clique em "Pets" para ver os pets disponíveis.
3. Clique em um pet para ver os detalhes.
4. Para solicitar adoção, faça cadastro ou login.

### Usuário comum

1. Acesse "Cadastre-se".
2. Crie uma conta.
3. Entre no sistema.
4. Acesse a lista de pets.
5. Abra o detalhe de um pet disponível.
6. Clique em "Solicitar adoção".
7. Escreva uma mensagem para a ONG.
8. Acompanhe o pedido em "Minhas solicitações".

### Administrador / ONG

1. Faça login com um usuário is_staff=True.
2. Acesse "Dashboard".
3. Use "Cadastrar pet" para adicionar novos pets.
4. Use a lista de pets para editar ou excluir cadastros.
5. Acesse "Solicitações" para ver todos os pedidos.
6. Abra uma solicitação e altere o status para:
   - Pendente;
   - Aprovada;
   - Recusada.

## Rotas Principais

text
/                                  Página inicial
/pets/                             Lista de pets
/pets/novo/                        Cadastrar pet, apenas admin
/pets/<id>/                        Detalhe do pet
/pets/<id>/editar/                 Editar pet, apenas admin
/pets/<id>/excluir/                Excluir pet, apenas admin
/pets/<id>/solicitar/              Solicitar adoção, usuário comum
/minhas-solicitacoes/              Solicitações do usuário comum
/solicitacoes/                     Todas as solicitações, apenas admin
/solicitacoes/<id>/status/         Alterar status da solicitação, apenas admin
/dashboard/                        Dashboard administrativo
/users/cadastro/                   Cadastro
/users/login/                      Login
/users/logout/                     Logout
/users/perfil/                     Perfil
/admin/                            Admin padrão do Django


## O Que Foi Testado e Funcionou

Foram testados os seguintes pontos:

- renderização da página inicial;
- renderização da lista de pets;
- cadastro de usuário comum;
- login e logout;
- acesso ao perfil;
- CRUD de pets para administrador;
- bloqueio de CRUD de pets para usuário comum;
- envio de solicitação de adoção por usuário comum;
- bloqueio de solicitação duplicada;
- bloqueio de solicitação feita por administrador;
- visualização das próprias solicitações pelo usuário comum;
- visualização de todas as solicitações pelo administrador;
- alteração de status da solicitação pelo administrador;
- atualização automática do status do pet após solicitação e aprovação;
- execução das migrations;
- execução dos testes automatizados.

Comandos usados para validação:

powershell
python manage.py check
python manage.py test
python manage.py migrate


Resultado esperado dos testes:

text
System check identified no issues
Ran 12 tests
OK


## Limitações Reconhecidas

- O projeto não possui JavaScript, conforme exigido no trabalho.
- O sistema não envia e-mails de confirmação.
- O sistema não possui recuperação de senha.
- O sistema não possui chat entre usuário e ONG.
- O sistema não possui filtro avançado por espécie, porte ou idade.

## Publicação

- Link do site publicado: https://adocao-pets.onrender.com
