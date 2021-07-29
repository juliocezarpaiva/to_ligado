from django.shortcuts import get_object_or_404
from to_ligado.settings import EMAIL_HOST_USER
from background_task.models import Task
from background_task import background
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import finances.views as finances_views

def delete_tasks(verbose_name):
    ''' Deleta tarefas previamente agendadas pelo usuário '''
    tasks = Task.objects.filter(verbose_name=verbose_name)
    if tasks:
        for task in tasks:
            task.delete()
    return 0

def create_task(request, quote_symbol, higher_limit, lower_limit, update_interval):
    ''' Cria uma tarefa de atualização/notificação usando os parametros inseridos pelo usuário, sendo eles: preço alto, preço baixo e intervalo '''
    user = get_object_or_404(User, pk=request.user.id)
    verbose_name="quote-"+quote_symbol+"-user-"+str(request.user.id)

    # remove as tarefas agendadas da ação especificada do usuário especificado antes de adicionar uma nova
    delete_tasks(verbose_name)
    # adiciona uma nova tarefa com agendamento 'update interval'*60 (x minutos * 60 - as tasks são agendadas em sengundos por padrão)
    update_and_notify(request.user.id, quote_symbol, higher_limit, lower_limit, verbose_name=verbose_name, creator=user, repeat=int(update_interval)*60, repeat_until=None)
    
    return 0

@background(schedule=5)
def update_and_notify(user_id, quote_symbol, higher_limit, lower_limit):
    ''' Atualiza os preços da ação do usuário através de uma requisição à API. Se o preço atingir algum dos valores definidos pelo usuário, dispara um email '''
    user = get_object_or_404(User, pk=user_id)
    # obtem a ação especificada por 'quote_symbol'
    updated_quote = finances_views.get_quote(quote_symbol)['quote']

    # se a açao for encontrada, cria um dicionário de dados vazio (isso evita que futuros erros aconteçam
    # quando uma ação encontrada pela API não tiver algum dos campos listados no dicionário)
    if updated_quote:
        quote_dict = {
            'shortName': '',
            'longName': '',
            'symbol': '',
            'currency': '',
            'regularMarketPrice': '',
            'regularMarketDayHigh': '',
            'regularMarketDayRange': '',
            'regularMarketDayLow': '',
            'regularMarketPreviousClose': '',
            'targetPriceHigh': '',
            'targetPriceLow': '',
            'targetPriceMean': '',
            'targetPriceMedian': '',
            'status': ''
        }
        # para cada chave do dicionário, atribui o valor se esse valor existir na ação.
        # caso não tenha valor, adicionar um '-' no intuito de exibir este caractere no email
        # simbolizando um campo vazio retornado pela API
        for key in quote_dict:
            print(key)
            if key in updated_quote:
                print('is in: ', key)
                quote_dict[key] = updated_quote[key]
            else:
                print('is not: ', key)
                quote_dict[key] = '-'

        # se o preço de mercado não é nulo (substituido anteriormente por '-')
        if quote_dict['regularMarketPrice'] != '-':
            # então atribui este valor, feito cast para float, em quote_price
            quote_price = float(quote_dict['regularMarketPrice'])
        else:
            # se o preço é nulo, atribui zero
            quote_price = 0
        # faz o cast dos valores higher e lower_price de str para float
        higher_price = float(higher_limit)
        lower_price = float(lower_limit)

        # se os valor de mercado atual da ação está entre os valores atribuidos pelo usuário, então notifica por email
        if quote_price >= higher_price or quote_price <= lower_price:
            # adiciona comprar/vender ao dicionario de dados para que o email sinalize a ação a ser tomada
            if quote_price >= higher_price: quote_dict['status'] = 'Essa é uma boa hora para você VENDER suas ações!'
            else:   quote_dict['status'] = 'Essa é uma boa hora para você COMPRAR ações!'

            # define o email a ser enviado renderizando o HTML notify/email.html com os valores repassados por quote_dict
            subject = 'Alerta de preços da TôLigado!'
            html_message = render_to_string('notify/email.html', quote_dict)
            message = render_to_string('notify/email.html', quote_dict)
            from_email = 'Da TôLigado! <' + EMAIL_HOST_USER + '>'
            
            # envia o email ao usuário autenticado
            user.email_user(subject, html_message=html_message, message=message, from_email=from_email)
            return 0
    else:
        return 1