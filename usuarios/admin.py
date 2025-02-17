from django.contrib import admin
from .models import Users, Professor, Encarregado, Aluno, Turma, Nota, Frequencia, Comunicacao, Evento
from django.contrib.auth import admin as admin_auth_django
from .forms import UserChangeForm, UserCreationForm

# Register your models here.

@admin.register(Users)
class UsersAdmin(admin_auth_django.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = Users
    fieldsets = admin_auth_django.UserAdmin.fieldsets + (
        ('Cargo', {'fields': ('cargo',)}),
    )
    list_display = admin_auth_django.UserAdmin.list_display + ('cargo',)
    
    
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user', 'disciplina',)
    list_filter = ('disciplina', 'formacao',)
    search_fields = ('disciplina', 'formacao', 'email',)
    
    
@admin.register(Encarregado)
class EncarregadoAdmin(admin.ModelAdmin):
    list_display = ('user', 'relacionamento_com_aluno', 'filho',)
    list_filter = ( 'relacionamento_com_aluno',)
    search_fields = ('relacionamento_com_aluno',)
    
    
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'turma',)
    list_filter = ('turma',)
    search_fields = ('nome', 'sobrenome')
    
    
@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'serie', 'curso','periodo', 'ano_letivo')
    list_filter = ('nome', 'serie', 'curso','periodo')
    search_fields = ('nome',)
    
    
@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('nota', 'aluno', 'turma', 'disciplina', 'semestre', 'tipo_prova', 'data_lancamento')
    list_filter = ('nota', 'turma', 'disciplina', 'semestre', 'tipo_prova', 'data_lancamento',)
    search_fields = ('turma', 'disciplina', 'semestre', 'tipo_prova', 'data_lancamento',)
    
@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'professor', 'turma', 'data', 'presente')
    list_filter = ('aluno', 'data', 'presente',)
    search_fields = ('aluno', 'presente',)
    
    
@admin.register(Comunicacao)
class ComunicacaoAdmin(admin.ModelAdmin):
    list_display = ('destinatario', 'remetente', 'assunto', 'data_envio')
    list_filter = ('data_envio', 'assunto',)
    search_fields = ('destinatario', 'remetente',)
    
    
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'data_inicio', 'data_fim', 'publico_alvo')
    list_filter = ('data_inicio', 'data_fim', 'publico_alvo',)
    search_fields = ('titulo', 'publico_alvo',)