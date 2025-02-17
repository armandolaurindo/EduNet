from rolepermissions.roles import AbstractUserRole

class Professor(AbstractUserRole):
    available_permissions = {
        'cadastrar_aluno': True,
        'ver_lista_alunos': True,
        'editar_info_aluno': True,
        'inserir_notas': True,
        'ver_notas': True,
        'editar_nota': True,
        'excluir_nota': True,
        'ver_desempenho_aluno': True,
        'ver_atividades': True,
    }
class Encarregado(AbstractUserRole):
    available_permissions = {
        'ver_notas': True,
        'ver_desempenho_aluno': True,
        'ver_atividades': True,
    }