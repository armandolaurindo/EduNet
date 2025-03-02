
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Users(AbstractUser):
    choices_cargo = (
                    ('P', 'Professor'),
                    ('E', 'Encarregado')
                )
    cargo = models.CharField(max_length=1, choices=choices_cargo, verbose_name="Tipo de Conta")
    
    def __str__(self):
        return f"{self.username} ({self.get_cargo_display()})"


# 📚 Tabela para Professores
class Professor(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="professor")
    disciplina = models.CharField(max_length=100, verbose_name="Disciplina")
    formacao = models.CharField(max_length=200, blank=True, null=True, verbose_name="Área Acadêmica")
    experiencia = models.TextField(blank=True, null=True, verbose_name="Experiência Profissional")
    data_contratacao = models.DateField(blank=True, null=True, verbose_name="Data de Contratação")
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.disciplina}"

# 🏫 Tabela de Turmas
class Turma(models.Model):
    ANO_LETIVO_CHOICES = [(str(ano), str(ano)) for ano in range(2000, 2051)]
    SERIE_CHOICES = [
        ('7ª Classe', '7ª Classe'),
        ('8ª Classe', '8ª Classe'),
        ('9ª Classe', '9ª Classe'),
        ('10ª Classe', '10º Classe'),
        ('11ª Classe', '11ª Classe'),
        ('12ª Classe', '12ª Classe'),
        ('13ª Classe', '13ª Classe'),
    ]
    PERIODO_CHOICES = [
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
        ('Noite', 'Noite'),
    ]
    CURSO_CHOICES = [
        ('Operador de informática', 'Operador de informática'),
        ('Auxiliar de contabilidade', 'Auxiliar de contabilidade'),
        ('Técnico de informática', 'Técnico de informática'),
        ('Informática de gestão', 'Informática de gestão'),
        ('Contabilidade de gestão', 'Contabilidade de gestão'),
        ('Finaças', 'Finaças'),
    ]
    nome = models.CharField(max_length=5, unique=True, verbose_name="Nome da turma")
    curso = models.CharField(max_length=30, choices=CURSO_CHOICES, verbose_name="Curso")
    ano_letivo = models.CharField(max_length=4, choices=ANO_LETIVO_CHOICES, verbose_name="Ano Letivo")
    serie = models.CharField(max_length=10, choices=SERIE_CHOICES, verbose_name="Classe")
    periodo = models.CharField(max_length=5, choices=PERIODO_CHOICES, verbose_name="Periódo")
    professor = models.ManyToManyField(Professor, null=True, blank=True, related_name="turmas", verbose_name="Professor")

    def __str__(self):
        return f"Turma: {self.nome} - {self.serie} -  {self.curso} - {self.periodo} ({self.ano_letivo})"
    
    
# 🎓 Tabela para Alunos (agora vinculados à turma)
class Aluno(models.Model):
    nome = models.CharField(max_length=50, verbose_name='Nome')
    sobrenome = models.CharField(max_length=50, verbose_name='Sobrenome')
    numero_matricula = models.CharField(max_length=20, unique=True, verbose_name="Número de Matrícula")
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True, related_name="alunos", verbose_name="Turma")
    

    def __str__(self):
        return f"Aluno: {self.nome} {self.sobrenome} - {self.turma}"
    

# 📊 Tabela de Notas
class Nota(models.Model):
    SEMESTRE_CHOICES = [
        ('1º Semestre', '1º Semestre'),
        ('2º Semestre', '2º Semestre'),
        ('3º Semestre', '3º Semestre')
    ]

    TIPO_PROVA_CHOICES = [
        ('Avaliação', 'Avaliação'),
        ('Prova do Professor', 'Prova do Professor'),
        ('Exame Final', 'Exame Final'),
        ('Recuperação', 'Recuperação')
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="notas")
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name="notas_lancadas")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="notas")
    disciplina = models.CharField(max_length=100, verbose_name="Disciplina")
    semestre = models.CharField(max_length=15, choices=SEMESTRE_CHOICES, verbose_name="Semestre")
    tipo_prova = models.CharField(max_length=20, choices=TIPO_PROVA_CHOICES, verbose_name="Tipo de Prova")
    nota = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="Nota")
    data_lancamento = models.DateField(auto_now_add=True, verbose_name="Data de Lançamento")

    def __str__(self):
        return f"Nota: {self.aluno.nome} {self.aluno.sobrenome} - {self.disciplina} - {self.semestre} - {self.tipo_prova}: {self.nota} - {self.data_lancamento.strftime('%d/%m/%Y')}"


# 👨‍👩‍👦 Tabela para Encarregados
class Encarregado(models.Model):
    relacao_choices = [('Pai', 'Pai'), ('Mãe', 'Mãe'), ('Outro', 'Outro')]
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="encarregado")
    filho = models.ForeignKey(Aluno, on_delete=models.SET_NULL, null=True, blank=True, related_name="encarregado", verbose_name="Filhos")
    relacionamento_com_aluno = models.CharField(max_length=50, choices=relacao_choices, verbose_name="Relação com o Aluno")

    def __str__(self):
        return f"Encarregado: {self.user.first_name} {self.user.last_name} ({self.relacionamento_com_aluno})"
    

# 📄 Tabela de Presença
class Frequencia(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="frequencias")
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name="frequencias_registradas")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="frequencias")
    data = models.DateField(auto_now_add=True, verbose_name="Data da Aula")
    presente = models.BooleanField(default=True, verbose_name="Presente?")

    def __str__(self):
        return f"Frequência: {self.aluno.user.first_name} {self.aluno.user.last_name} - {self.data} - {'Presente' if self.presente else 'Faltou'}"


# 📬 Tabela de Comunicação
class Comunicacao(models.Model):
    destinatario = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="mensagens_recebidas")
    remetente = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="mensagens_enviadas")
    assunto = models.CharField(max_length=200, verbose_name="Assunto")
    mensagem = models.TextField(verbose_name="Mensagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")

    def __str__(self):
        return f"Mensagem de {self.remetente.first_name} {self.remetente.last_name} para {self.destinatario.first_name} {self.destinatario.last_name}"

# 📅 Tabela de Eventos e Calendário Escolar
class Evento(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    data_inicio = models.DateTimeField(verbose_name="Data de Início")
    data_fim = models.DateTimeField(blank=True, null=True, verbose_name="Data de Fim")
    publico_alvo = models.CharField(max_length=50, choices=[('Todos', 'Todos'), ('Professores', 'Professores'), ('Alunos', 'Alunos'), ('Encarregados', 'Encarregados')], verbose_name="Público Alvo")

    def __str__(self):
        return f"Evento: {self.titulo} - {self.data_inicio.strftime('%d/%m/%Y')}"
