from to_ligado.settings import X_RAPIDAPI_KEY, X_RAPIDAPI_HOST
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .notify import *
from .models import UserQuotes
import http.client, json

# autenticação da API de consulta de ações da Yahoo Finance
conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")
headers = { 'x-rapidapi-key': X_RAPIDAPI_KEY, 'x-rapidapi-host': X_RAPIDAPI_HOST }

def market(request):
    """ Consulta a API procurando por informações sobre o mercado """
    conn.request("GET", "/market/v2/get-summary?region=BR", headers=headers)
    res = conn.getresponse()
    data = res.read()
    summary = json.loads(data.decode("utf-8"))['marketSummaryAndSparkResponse']
    return render(request, 'finances/summary.html', { 'summary': summary['result'] })
    
def search_quotes(request, currency):
    """ Consulta a API procurando por ações que contenham o campo 'currency' no nome """
    # verifica se a barra de pesquisa foi preenchida ou se está vazia
    if currency:
        conn.request("GET", "/auto-complete?q="+currency+"&region=BR", headers=headers)
        res = conn.getresponse()
        data = res.read()
        api_quotes = json.loads(data.decode("utf-8"))['quotes']
        # verifica se o usuário quer procurar somente na B3 ou se quer procurar globalmente utilizando selector na página
        if 'onlyB3' in request.GET:
            if request.GET['onlyB3'] == '1':
                SA_quotes = [ { key: quote[key] for key in quote } for quote in api_quotes if quote['exchange'] == 'SAO' or quote['symbol'].endswith('.SA') ]
                return { 'quotes': SA_quotes }
        return { 'quotes': api_quotes }
    else:
        # se a pesquisa é vazia retorna um dicionario nulo
        return { 'quotes': {} }

def get_quote(quote):
    """ Consulta a API em busca da ação a partir do símbolo 'quote' """
    conn.request("GET", "/market/v2/get-quotes?region=BR&symbols="+quote, headers=headers)
    res = conn.getresponse()
    data = res.read()
    api_quote = json.loads(data.decode("utf-8"))['quoteResponse']
    return { 'quote': api_quote['result'][0] }

# nao utilizada
def get_chart(quote, interval, time_range):
    """ Consulta a API em busca de gráficos a partir do símbolo 'quote', do intervalo 'interval' e do alcance 'time_range' """
    conn.request("GET", "/market/get-charts?symbol="+quote+"&interval="+interval+"&range="+time_range+"&region=BR", headers=headers)
    res = conn.getresponse()
    data = res.read()
    api_chart = json.loads(data.decode("utf-8"))['chart']
    return { 'chart': api_chart }

def search(request):
    """ Busca por ações com 'search_quotes' através de da aticação da barra de buscas """
    if 'search' in request.GET:
        currency = request.GET['search']
        if currency.strip():
            currency = currency.replace(' ', '-')
    else:
        currency = ''
    return render(request, 'finances/list.html', search_quotes(request, currency))

def my_quotes(request):
    """ Busca por ações com 'search_quotes' através de da aticação da barra de buscas """
    quotes = UserQuotes.objects.filter(user = request.user.id)
    quote_list = ''
    for quote in quotes:
        quote_list += quote.symbol + '%2C'

    return render(request, 'finances/list.html', search_quotes(request, quote_list))

def quote_dashboard(request, quote_symbol):
    """ Renderiza a quote_dashboard de cada ação 'quote' com informações coletadas através do método 'get_quote' """
    if quote_symbol.strip():
        try:
            user_quote = UserQuotes.objects.get(symbol=quote_symbol, user_id=request.user.id)
            quote = { 'quote': get_quote(quote_symbol), 'user_quote': user_quote }
        except UserQuotes.DoesNotExist:
            quote = { 'quote': get_quote(quote_symbol), 'user_quote': {} }
        # se o usuario tem quote salva entao preenche o form de configuração da quote no front
        return render(request, 'finances/board.html', quote)
    else:
        messages.error(request, 'Algo deu errado, tente buscar a ação novamente')
        return redirect('quote_dashboard')

def create_user_quote(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.id)

        higher_limit = float((request.POST['higher_limit']).replace(',','.'))
        lower_limit = float((request.POST['lower_limit']).replace(',','.'))

        quote = {
            'symbol': request.POST['symbol'],
            'update_interval': request.POST['update_interval'],
            'higher_limit': higher_limit,
            'lower_limit': lower_limit
        }

        # busca UserQuote pelo symbol e pelo user, se não acha, então cria um com os parametros em defaults
        obj, created = UserQuotes.objects.get_or_create(
            symbol=quote['symbol'],
            user = user,
            defaults={
                'symbol': quote['symbol'],
                'update_interval': quote['update_interval'],
                'higher_limit': quote['higher_limit'],
                'lower_limit': quote['lower_limit'],
                'notification_check': True,
                'user': user
            },
        )
        # se não criou um UserQuote, ou seja, já existe, então atualiza a UserQuote encontrada
        if not created:
            obj.symbol = quote['symbol']
            obj.update_interval = quote['update_interval']
            obj.higher_limit = quote['higher_limit']
            obj.lower_limit = quote['lower_limit']
            obj.notification_check = True
            obj.save()

        # cria a ação de atualização e notificação usando a backgroud_tasks
        create_task(request, quote['symbol'], quote['higher_limit'], quote['lower_limit'], quote['update_interval'])

        return redirect('quote_dashboard', quote['symbol'])

def remove_user_quote(request, quote_symbol):
    verbose_name="quote-"+quote_symbol+"-user-"+str(request.user.id)
    # encontra a ação
    quote = UserQuotes.objects.get(symbol=quote_symbol, user_id=request.user.id)
    if quote:
        # deleta ação
        quote.delete()
    # deleta o tarefa de atualização e notificação
    delete_tasks(verbose_name)
    return redirect('my_quotes')
