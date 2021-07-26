from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.shortcuts import get_object_or_404, render, redirect

def empty_field(request, field, message, route):
    if not field.strip():
        print('vazio')
        messages.error(request, message)
        return redirect(route)

def register(request):
    """ Cadastra um novo usuário no sistema """
    # se o usuário está logado, mas, por algum motivo consegue acessar a rota de registro,
    # então redireciona direto para a dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            # recebe campos username, email e senha atraves da req POST
            username = request.POST['user']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            # se algum dos campos do form for nulo, imprime mensagem de erro e redireciona de volta ao login
            empty_field(request, username, 'Insira um nome de usuário válido', 'register')
            empty_field(request, email, 'Insira um email válido', 'register')
            empty_field(request, password, 'Insira uma senha válida', 'register')

            # verifica se as senhas coincidem
            if password != password2:
                messages.error(request, 'As senhas não são iguais')
                return redirect('register')

            # verifica se o email desejado já não foi utilizado
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este email já foi usado')
                return redirect('register')

            # verifica se o username desejado já não foi utilizado
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Este nome de usuário já foi usado')
                return redirect('register')

            # realiza a criação de conta
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso')
            
            # tenta fazer a autenticação
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
        
        # renderiza formulário de registro
        return render(request, 'users/register.html')

def login(request):
    """ Realiza o processo de autenticação """
    # se o usuário está logado, mas, por algum motivo consegue acessar a rota de login,
    # então redireciona direto para a dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            # recebe campos username e senha atraves da req POST
            username = request.POST['username']
            password = request.POST['password']

            # se algum dos campos do form for nulo, imprime mensagem de erro e redireciona de volta ao login
            empty_field(request, username, 'Seu nome de usuário não pode estar em branco', 'login')
            empty_field(request, password, 'Sua senha não pode estar em branco', 'login')

            # tenta fazer a autenticação
            user = auth.authenticate(request, username=username, password=password)
            # se consegue se logar, então redireciona para dashboard
            # caso não consiga, redireciona de volta para o login
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Algo deu errado. Tente logar novamente')
                return redirect('login')
        
        # renderiza formulário de login
        return render(request, 'users/login.html')

def dashboard(request):
    """ Exibe a dashboard para o usuário autenticado """
    if request.user.is_authenticated:
        return render(request, 'users/dashboard.html')
    else:
        return redirect('home')

def logout(request):
    """ Realiza o processo de logout """
    auth.logout(request)
    return redirect('home')

def update_user(request):
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
        empty_field(request, old_password, 'Preencha o campo da sua senha atual', 'update_user')
        # se preencheu, dá continuidade no processo de atualização
        if not user.check_password(old_password):
            # se a senha atual estiver incorreta, emite mensagem e retorna para o formulario
            messages.error(request, 'Senha incorreta')
            return redirect('update_user')
        else:
            # se a senha atual está correta, avança no processo
            # verifica se tem senha para ser atualizada
            if new_password.strip() or new_password2.strip():
                # verifica se as senhas coincidem
                if new_password != new_password2:
                    messages.error(request, 'As senhas não são iguais')
                    return redirect('update_user')
                else:
                    # se as senhas coincidirem, atualiza a senha
                    user.set_password(new_password)

            # verifica se tem nome e sobrenome preenchidos
            empty_field(request, first_name, 'Preencha os campos de nome', 'update_user')
            empty_field(request, last_name, 'Preencha os campos de nome', 'update_user')
            # se tudo foi preenchido corretamente e a senha foi validada, continua com o processo
            user.first_name = first_name
            user.last_name = last_name
            # atualiza o usuário
            user.save()
            messages.success(request, 'Perfil atualizado com sucesso')
            
            # refaz a autenticação
            if user is not None:
                auth.login(request, user)
                return redirect('update_user')
    else:
        # renderiza formulario de edição de dados
        return render(request, 'users/profile.html')