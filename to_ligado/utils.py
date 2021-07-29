from django.contrib import messages
from django.shortcuts import redirect

def empty_field(field):
    """ Verifica se o campo está vazio """
    if not field.strip():   return True
    else:   return False

def send_error(request, message, page):
    """ Envia mensagem de erro e redireciona para a página 'page' """
    messages.error(request, message)
    return redirect(page)

def send_success(request, message, page):
    """ Envia mensagem de sucesso e redireciona para a página 'page' """
    messages.success(request, message)
    return redirect(page)