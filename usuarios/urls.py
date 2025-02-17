from django.urls import path
from . import views

urlpatterns = [
    path('entrar/', views.entrar, name='entrar'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('sair/', views.sair, name='sair'),
    # urls professores
    path('turmas/', views.turmas, name='turmas'),
    path('turma/<str:id_turma>/', views.turma, name='turma'),
    path('cadastrar_aluno/<str:id_t>', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('atualizar_aluno/', views.att_aluno, name='att_aluno'),
    path('update_aluno/<str:id_a>', views.update_aluno, name="update_aluno"),
    # urls encarregados
    path('encontrar_aluno/', views.encontrar_aluno, name='encontrar_aluno'),
    path('desempenho_aluno/', views.desempenho_aluno, name='desempenho_aluno'),
]
