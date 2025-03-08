from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rolepermissions.decorators import has_permission_decorator, has_role_decorator
from .models import Users, Professor, Aluno, Encarregado, Turma, Nota, Frequencia
from django.shortcuts import redirect, reverse
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib import messages
import json


def entrar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            if request.user.cargo == 'P':
                return redirect(reverse('turmas'))
            elif request.user.cargo == 'E':
                return redirect(reverse('encontrar_aluno'))
        return render(request, 'login.html')
    elif request.method == "POST":
        login = request.POST.get('email')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(username=login, password=senha)
        if not user:
            messages.add_message(request, messages.ERROR, 'Usuário não existe.')
            return redirect(reverse('entrar'))
        
        auth.login(request, user)
        if request.user.cargo == 'P':
            return redirect(reverse('turmas'))
        elif request.user.cargo == 'E':
            return redirect(reverse('encontrar_aluno'))
    

def cadastrar(request):
    if request.method == "GET":
        typy_cargo_user = Users.choices_cargo
        relacoes = Encarregado.relacao_choices
        return render(request, 'register.html', {'typy_cargo_user': typy_cargo_user, 'relacoes': relacoes})
    elif request.method == "POST":
        nome = request.POST.get('first_name')
        sobrenome = request.POST.get('last_name')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        cargo = request.POST.get('cargo')
        
        if cargo == 'P':
            disciplina = request.POST.get('disciplina')
            if disciplina == '':
                messages.add_message(request, messages.WARNING, 'Porfavor, preencha todos os campos.')
                return redirect(reverse('cadastrar'))
            print(disciplina)
        elif cargo == 'E':
            relacao_com_filho = request.POST.get('relacao_com_aluno')
            if relacao_com_filho == '':
                messages.add_message(request, messages.WARNING, 'Porfavor, preencha todos os campos.')
                return redirect(reverse('cadastrar'))
            print(relacao_com_filho)
        
        datas = [nome, sobrenome, email, senha, cargo]
        for data in datas:
            if data == '':
                messages.add_message(request, messages.WARNING, 'Porfavor, preencha todos os campos.')
                return redirect(reverse('cadastrar'))
        
        user = Users.objects.filter(email=email)
        if user.exists():
            messages.add_message(request, messages.ERROR, 'E-mail já existente.')
            return redirect(reverse('cadastrar'))
        
        user = Users.objects.create_user(
            username=email, 
            email=email, 
            password=senha, 
            first_name=nome,
            last_name=sobrenome,
            cargo=cargo
        )
        if cargo == 'P':
            disciplina = request.POST.get('disciplina')
            professor = Professor(user=user, disciplina=disciplina)
            professor.save()
        elif cargo == 'E':
            relacao_com_filho = request.POST.get('relacao_com_aluno')
            encarregado = Encarregado(user=user, relacionamento_com_aluno=relacao_com_filho)
            encarregado.save()
        
        messages.add_message(request, messages.SUCCESS, 'Conta criada com sucesso, entre para continuares')
        return redirect(reverse('entrar'))
    

def sair(request):
    request.session.flush()
    return redirect(reverse('entrar'))


@has_role_decorator('professor')
def turmas(request):
    if request.method == "GET":
        turmas = Turma.objects.filter(professor=request.user.professor)
        return render(request, 'turmas.html', {'turmas': turmas})
    

@has_role_decorator('professor')
def turma(request, id_turma):
    if request.method == "GET":
        turma = Turma.objects.get(id=id_turma)
        alunos = Aluno.objects.filter(turma=id_turma)
        return render(request, 'turma.html', {'turma': turma, 'alunos': alunos})
    
    
@has_role_decorator('professor')
def inserir_notas(request, id_aluno):
    if request.method == 'GET':
        aluno = Aluno.objects.get(id=id_aluno)
        t_prova = Nota.TIPO_PROVA_CHOICES
        semestre = Nota.SEMESTRE_CHOICES
        notas_aluno = Nota.objects.filter(aluno=aluno)
        return render(request, 'inserir_notas.html', {'aluno': aluno, 'tipo_prova': t_prova, 'semestres': semestre, 'all_notas': notas_aluno})
    elif request.method == 'POST':
        valor_nota = request.POST.get('nota')
        type_prova = request.POST.get('tipo-prova')
        semestre = request.POST.get('semestre')
        
        disciplina = request.user.professor.disciplina
        professor = request.user.professor
        aluno = Aluno.objects.get(id=id_aluno)
        turma = aluno.turma
        
        valor = str(valor_nota).replace(',', '.')
        
        nota = Nota(
            disciplina=disciplina,
            professor=professor,
            turma=turma,
            aluno=aluno,
            semestre=semestre,
            tipo_prova=type_prova,
            nota=valor,
        )
        nota.save()
        
        messages.add_message(request, messages.SUCCESS, 'A nota foi adicionada!')
        return redirect(reverse('inserir_notas', args=id_aluno))

@has_role_decorator('professor')
def atualizar_nota(request):
    id_nota = request.POST.get('id_nota')
    nota = Nota.objects.filter(id=id_nota)
    nota_json = json.loads(serializers.serialize('json', nota))[0]['fields']
    nota_id = json.loads(serializers.serialize('json', nota))[0]['pk']
    data = {'nota': nota_json, 'nota_id': nota_id}
    return JsonResponse(data)

@has_role_decorator('professor')
def update_nota(request, id_nota):
    body = json.loads(request.body)
    valor_nota = body['nota']
    nota = get_object_or_404(Nota, id=id_nota)

    try:
        nota.nota = valor_nota
        nota.save()
        return JsonResponse({'status': '200', 'nota': valor_nota})
    except:
        return JsonResponse({'status': '500' })
    
'''
@has_permission_decorator('cadastrar_aluno') 
def cadastrar_aluno(request, id_t):
    turma = Turma.objects.get(id=id_t)
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    num_matricula = request.POST.get('num_marticula')
    
    aluno = Aluno.objects.filter(numero_matricula=num_matricula)
    if aluno.exists():
        messages.add_message(request, messages.ERROR, 'Já existe um aluno(a) com esta matrícula.')
        return redirect(reverse('turma', args=id_t))
    
    aluno = Aluno(
        nome=nome,
        sobrenome=sobrenome,
        numero_matricula=num_matricula,
        turma=turma,
    )
    aluno.save()
    
    messages.add_message(request, messages.SUCCESS, 'Aluno(a) cadastrardo(a) com sucesso!')
    return redirect(reverse('turma', args=id_t))


def att_aluno(request):
    id_aluno = request.POST.get('id_aluno')
    aluno = Aluno.objects.filter(id=id_aluno)
    aluno_json = json.loads(serializers.serialize('json', aluno))[0]['fields']
    print(aluno_json) #TODO: não pode retornar o mesmo id
    aluno_id = json.loads(serializers.serialize('json', aluno))[0]['pk']
    print(aluno_id)
    data = {'aluno': aluno_json, 'aluno_id': aluno_id}
    return JsonResponse(data)


def update_aluno(request, id_a):
    body = json.loads(request.body)
    print(body)
    nome = body['nome']
    sobrenome = body['sobrenome']
    numero_matricula = body['numero_matricula']
    
    lista_dados = [nome, sobrenome, numero_matricula]
    aluno = get_object_or_404(Aluno, id=id_a)
    
    for dado in lista_dados:
        if dado == '':
            messages.add_message(request, messages.INFO, 'Preecha todos os campos.')
            return redirect(reverse('turma', args=id_a))

    try:
        aluno.nome = nome
        aluno.sobrenome = sobrenome
        aluno.numero_matricula = numero_matricula
        aluno.save()
        return JsonResponse({'status': '200', 'nome': nome, 'sobrenome': sobrenome, 'numero_matricula': numero_matricula})
    except:
        return JsonResponse({'status': '500' })
'''


# para o encarregado
@has_role_decorator('encarregado')
def encontrar_aluno(request):
    return render(request, 'encontrar_aluno.html')


@has_permission_decorator('ver_desempenho_aluno')
def desempenho_aluno(request):
    return render(request, 'desempenho_aluno.html')
