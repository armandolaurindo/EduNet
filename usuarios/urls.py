from django.urls import path
from . import views

urlpatterns = [
    path('entrar/', views.entrar, name='entrar'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('sair/', views.sair, name='sair'),
    # urls professores
    path('turmas/', views.turmas, name='turmas'),
    path('turma/<str:id_turma>/', views.turma, name='turma'),
    path('inserir_notas/<str:id_aluno>/', views.inserir_notas, name='inserir_notas'),
    path('atualizar_nota/', views.atualizar_nota, name='atualizar_nota'),
    path('update_nota/<str:id_nota>', views.update_nota, name='update_nota'),
    # urls encarregados
    path('encontrar_aluno/', views.encontrar_aluno, name='encontrar_aluno'),
    path('desempenho_aluno/', views.desempenho_aluno, name='desempenho_aluno'),
]
