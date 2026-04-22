# PetAdoção

Sistema web de adoção de pets desenvolvido em **Python + Django**, com **HTML e CSS**, para a disciplina de Programação Web.

O projeto não utiliza JavaScript e foi construído com foco acadêmico: código simples, navegação clara, CRUD completo, autenticação e controle de acesso por tipo de usuário.

## Integrantes

- Nome do integrante 1: preencher
- Nome do integrante 2: preencher, se houver

## Links da Entrega

- Site publicado: preencher com o link do Render
- Repositório público: preencher com o link do GitHub

## Tecnologias

- Python
- Django
- HTML
- CSS
- SQLite localmente
- PostgreSQL no Render, quando `DATABASE_URL` estiver configurada
- WhiteNoise para arquivos estáticos
- Gunicorn para execução em produção
- Pillow para upload de imagens

## Perfis de Usuário

### Usuário comum

Usuários comuns são contas com `is_staff=False`.

Podem:

- criar conta;
- fazer login e logout;
- visualizar pets disponíveis;
- acessar detalhes dos pets;
- solicitar adoção;
- visualizar apenas as próprias solicitações.

### Administrador / ONG

Administradores são usuários com `is_staff=True`.

Podem:

- acessar o dashboard;
- cadastrar pets;
- editar pets;
- excluir pets;
- visualizar todos os pets;
- visualizar todas as solicitações;
- aprovar ou recusar solicitações.

## Funcionalidades

- Cadastro de usuários.
- Login e logout.
- Perfil do usuário.
- Página inicial com pets em destaque.
- CRUD completo de pets.
- Upload opcional de foto do pet.
- Listagem pública de pets disponíveis.
- Detalhes do pet.
- Solicitação de adoção por usuário comum.
- Bloqueio de solicitação duplicada para o mesmo pet.
- Listagem de solicitações do usuário comum.
- Listagem geral de solicitações para admin.
- Alteração de status da solicitação pelo admin.
- Atualização automática do status do pet conforme o andamento da adoção.

## Regras de Negócio

### Pet

Campos principais:

- nome;
- idade;
- porte;
- espécie;
- raça;
- descrição;
- status;
- foto;
- data de cadastro.

Choices:

- Porte: Pequeno, Médio, Grande.
- Espécie: Cachorro, Gato.
- Status: Disponível, Em processo de adoção, Adotado.

### Solicitação de Adoção

Campos principais:

- usuário;
- pet;
- mensagem;
- status;
- data da solicitação.

Choices:

- Pendente;
- Aprovada;
- Recusada.

Regras:

- o mesmo usuário não pode solicitar adoção do mesmo pet mais de uma vez;
- ao criar uma solicitação, o pet fica "Em processo de adoção";
- ao aprovar uma solicitação, o pet fica "Adotado";
- ao recusar uma solicitação, o pet volta para "Disponível".

## Estrutura do Projeto

```text
adocao_pets/
├── build.sh
├── Procfile
├── manage.py
├── requirements.txt
├── README.md
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── pets/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── templates/pets/
│       ├── admin_dashboard.html
│       ├── atualizar_status_solicitacao.html
│       ├── home.html
│       ├── listar_solicitacoes.html
│       ├── minhas_solicitacoes.html
│       ├── pet_confirm_delete.html
│       ├── pet_detail.html
│       ├── pet_form.html
│       ├── pet_list.html
│       └── solicitacao_form.html
├── users/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── management/commands/
│   │   └── ensure_admin.py
│   ├── migrations/
│   └── templates/users/
│       ├── login.html
│       ├── perfil.html
│       └── register.html
├── templates/
│   └── base.html
├── static/
│   ├── css/style.css
│   └── img/
└── media/
    └── pets/
```

## Como Rodar Localmente

### 1. Acessar o projeto

```powershell
cd c:\Users\gsant\dev\adocao_pets
```

### 2. Ativar a venv

```powershell
.\venv\Scripts\activate
```

### 3. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 4. Aplicar migrations

```powershell
python manage.py migrate
```

### 5. Criar ou atualizar o admin padrão

```powershell
python manage.py ensure_admin
```

Por padrão acadêmico, o comando cria um superusuário com:

```text
Usuário: testeadmin
Senha: vascodagama123
```

Também é possível sobrescrever esses dados por variáveis de ambiente:

```text
DJANGO_SUPERUSER_USERNAME
DJANGO_SUPERUSER_EMAIL
DJANGO_SUPERUSER_PASSWORD
```

### 6. Rodar o servidor

```powershell
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Manual de Uso

### Visitante

1. Acessa a página inicial.
2. Abre a lista de pets.
3. Visualiza os detalhes dos pets disponíveis.
4. Para solicitar adoção, precisa criar conta ou fazer login.

### Usuário comum

1. Acessa "Cadastre-se".
2. Cria uma conta.
3. Faz login.
4. Abre a lista de pets.
5. Entra no detalhe de um pet disponível.
6. Clica em "Solicitar adoção".
7. Envia uma mensagem.
8. Acompanha o pedido em "Minhas solicitações".

### Administrador / ONG

1. Faz login com usuário admin.
2. Acessa "Dashboard".
3. Cadastra novos pets.
4. Edita ou exclui pets pela tela de detalhes.
5. Acessa "Solicitações".
6. Aprova ou recusa pedidos de adoção.

## Rotas Principais

```text
/                                  Página inicial
/pets/                             Lista de pets
/pets/novo/                        Cadastrar pet
/pets/<id>/                        Detalhe do pet
/pets/<id>/editar/                 Editar pet
/pets/<id>/excluir/                Excluir pet
/pets/<id>/solicitar/              Solicitar adoção
/minhas-solicitacoes/              Solicitações do usuário comum
/solicitacoes/                     Solicitações para admin
/solicitacoes/<id>/status/         Atualizar status da solicitação
/dashboard/                        Dashboard administrativo
/users/cadastro/                   Cadastro
/users/login/                      Login
/users/logout/                     Logout
/users/perfil/                     Perfil
/admin/                            Admin padrão do Django
```

## Deploy no Render

O projeto está preparado para deploy no Render.

Arquivos usados:

- `build.sh`
- `Procfile`

Configuração no Render:

```text
Build Command: bash build.sh
Start Command: gunicorn config.wsgi:application
```

O `build.sh` executa:

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py ensure_admin
```

Variáveis recomendadas:

```text
SECRET_KEY=uma-chave-secreta-forte
DEBUG=False
ALLOWED_HOSTS=seu-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://seu-app.onrender.com
DATABASE_URL=url-do-postgresql-do-render
SECURE_SSL_REDIRECT=True
```

O Render também fornece `RENDER_EXTERNAL_HOSTNAME`, que o projeto usa automaticamente em `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.

## Upload de Fotos no Render

O projeto serve arquivos de `media/` também com `DEBUG=False`, por meio da configuração:

```python
SERVE_MEDIA_FILES = True
```

Isso permite visualizar fotos cadastradas no Render, como:

```text
/media/pets/nome-da-foto.jpg
```

Observação: em produção real, o ideal seria usar Cloudinary, S3 ou outro serviço externo. Para este trabalho acadêmico, a rota de mídia atende ao teste funcional no Render.

## Testes

Foram criados testes automatizados para autenticação, permissões, CRUD protegido e solicitações de adoção.

Comandos:

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --no-input
```

Resultado esperado:

```text
System check identified no issues
Ran 13 tests
OK
```

## O Que Foi Testado e Funcionou

- Página inicial.
- Lista de pets.
- Detalhe de pet.
- Cadastro de usuário comum.
- Login e logout.
- Perfil.
- CRUD de pets para admin.
- Bloqueio de CRUD para usuário comum.
- Solicitação de adoção por usuário comum.
- Bloqueio de solicitação duplicada.
- Bloqueio de solicitação feita por admin.
- Listagem das próprias solicitações.
- Listagem geral de solicitações para admin.
- Aprovação de solicitação.
- Atualização automática do status do pet.
- Upload e exibição de foto localmente.
- Exibição de foto em `/media/` no Render.
- Deploy com `collectstatic`, `migrate` e criação de admin via `ensure_admin`.

## Limitações Conhecidas

- O projeto não usa JavaScript, conforme exigido.
- Não há recuperação de senha.
- Não há envio de e-mails.
- Não há chat entre usuário e ONG.
- Não há filtros avançados por porte, espécie ou idade.
- Uploads em `media/` no Render podem depender do armazenamento disponível no serviço. Para produção real, recomenda-se um serviço externo de mídia.
- O superusuário padrão foi criado para facilitar a avaliação acadêmica. Em um sistema real, a senha deve ser definida somente por variável de ambiente e alterada após o primeiro acesso.

## Requisitos do Trabalho Atendidos

- Site em Python + Django.
- HTML e CSS.
- Sem JavaScript.
- CRUD completo.
- Banco de dados.
- Login.
- Visões diferentes por tipo de usuário.
- Gerência de usuário.
- Publicação no Render.
- README com escopo, funcionamento, testes e limitações.

