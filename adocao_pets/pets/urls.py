from django.urls import path

from . import views

app_name = 'pets'

urlpatterns = [
    path('pets/', views.pet_list_view, name='pet_list'),
    path('pets/novo/', views.pet_create_view, name='pet_create'),
    path('pets/<int:pk>/', views.pet_detail_view, name='pet_detail'),
    path('pets/<int:pk>/editar/', views.pet_update_view, name='pet_update'),
    path('pets/<int:pk>/excluir/', views.pet_delete_view, name='pet_delete'),
]
