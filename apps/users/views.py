from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from to_ligado.utils import *

def register(request):
    """ Cadastra um novo usuário no sistema """
    # se o usuário está logado, mas, por algum motivo consegue acessar a rota de registro,
    # então redireciona direto para a dashboard
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            # recebe campos username, email e senha atraves da req POST
            username = request.POST['user']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            # se algum dos campos do form for nulo, imprime mensagem de erro e redireciona de volta ao login
            if empty_field(username):   send_error(request, 'Insira um nome de usuário válido', 'register')
            if empty_field(first_name): send_error(request, 'Insira um nome válido', 'register')
            if empty_field(last_name):  send_error(request, 'Insira um sobrenome válido', 'register')
            if empty_field(email):      send_error(request, 'Insira um email válido', 'register')
            if empty_field(password):   send_error(request, 'Insira uma senha válida', 'register')

            # verifica se as senhas coincidem
            if password != password2:   send_error(request, 'As senhas não são iguais', 'register')

            # verifica se o email desejado já não foi utilizado
            if User.objects.filter(email=email).exists():   send_error(request, 'Este email já foi usado', 'register')

            # verifica se o username desejado já não foi utilizado
            if User.objects.filter(username=username).exists(): send_error(request, 'Este nome de usuário já foi usado', 'register')

            # realiza a criação de conta
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()
            
            # tenta fazer a autenticação
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                send_success(request, 'Usuário cadastrado com sucesso', 'home')
        
        # renderiza formulário de registro
        return render(request, 'users/register.html')

def login(request):
    """ Realiza o processo de autenticação """
    # se o usuário está logado, mas, por algum motivo consegue acessar a rota de login,
    # então redireciona direto para a dashboard
    if request.user.is_authenticated:
        return redirect('my_quotes')
    else:
        if request.method == 'POST':
            # recebe campos username e senha atraves da req POST
            username = request.POST['username']
            password = request.POST['password']
            
            # se algum dos campos do form for nulo, imprime mensagem de erro e redireciona de volta ao login
            if empty_field(username):   send_error(request, 'Seu nome de usuário não pode estar em branco', 'login')
            if empty_field(password):   send_error(request, 'Sua senha não pode estar em branco', 'login')

            # tenta fazer a autenticação
            user = auth.authenticate(request, username=username, password=password)
            # se consegue se logar, então redireciona para a lista de ações
            # caso não consiga, redireciona de volta para o login
            if user is not None:
                auth.login(request, user)
                return redirect('my_quotes')
            else:
                messages.error(request, 'Algo deu errado. Tente logar novamente')
                return redirect('login')
        
        # renderiza formulário de login
        return render(request, 'users/login.html')

def logout(request):
    """ Realiza o processo de logout """
    auth.logout(request)
    return redirect('home')

def profile(request):
    """ Realiza o processo de atualização dos dados do usuário """
    if request.user.is_authenticated:
        user = request.user
    else:
        messages.error(request, 'Você não tem permição para acessar essa página')
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        old_password = request.POST['password']
        new_password = request.POST['new_password']
        new_password2 = request.POST['new_password2']

        # verifica se o usuário preencheu a senha atual
        if empty_field(old_password):   send_error(request, 'Preencha o campo da sua senha atual', 'profile')
        # se preencheu, dá continuidade no processo de atualização
        if not user.check_password(old_password):
            # se a senha atual estiver incorreta, emite mensagem e retorna para o formulario
             send_error(request, 'Senha incorreta', 'profile')
        else:
            # se a senha atual está correta, avança no processo
            # verifica se tem senha para ser atualizada
            if new_password.strip() or new_password2.strip():
                # verifica se as senhas coincidem
                if new_password != new_password2:    send_error(request, 'As senhas não são iguais', 'profile')
                else:
                    # se as senhas coincidirem, atualiza a senha
                    user.set_password(new_password)

            # verifica se tem nome e sobrenome preenchidos
            if empty_field(first_name) or empty_field(last_name): send_error(request, 'Preencha os campos de nome', 'profile')
            # se tudo foi preenchido corretamente e a senha foi validada, continua com o processo
            user.first_name = first_name
            user.last_name = last_name
            # atualiza o usuário
            user.save()
            
            # refaz a autenticação
            if user is not None:
                auth.login(request, user)
                send_success(request, 'Perfil atualizado com sucesso', 'profile')
    else:
        # renderiza formulario de edição de dados
        return render(request, 'users/profile.html')