from django.urls import path

from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('pets/', views.pet_list_view, name='pet_list'),
    path('pets/novo/', views.pet_create_view, name='pet_create'),
    path('pets/<int:pk>/', views.pet_detail_view, name='pet_detail'),
    path('pets/<int:pk>/editar/', views.pet_update_view, name='pet_update'),
    path('pets/<int:pk>/excluir/', views.pet_delete_view, name='pet_delete'),
    path(
        'pets/<int:pet_pk>/solicitar/',
        views.criar_solicitacao_view,
        name='criar_solicitacao',
    ),
    path(
        'minhas-solicitacoes/',
        views.minhas_solicitacoes_view,
        name='minhas_solicitacoes',
    ),
    path(
        'solicitacoes/',
        views.listar_solicitacoes_view,
        name='listar_solicitacoes',
    ),
    path(
        'solicitacoes/<int:pk>/status/',
        views.atualizar_status_solicitacao_view,
        name='atualizar_status_solicitacao',
    ),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
]
