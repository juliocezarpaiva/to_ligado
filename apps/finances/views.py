from django.contrib import messages
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import UserQuotes
import http.client, json

# autenticação da API de consulta de ações da Yahoo Finance
conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "f130a4cc6cmsh12088d8d4aefa12p1ff271jsnae4fadeb438e",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

def market(request):
    conn.request("GET", "/market/v2/get-summary?region=BR", headers=headers)
    res = conn.getresponse()
    data = res.read()
    summary = json.loads(data.decode("utf-8"))['marketSummaryAndSparkResponse']
    return render(request, 'finances/summary.html', { 'summary': summary['result'] })
    
def search_quotes(request, currency):
    """ Consulta a API procurando por ações que contenham o campo 'currency' no nome """
    # verifica se a barra de pesquisa foi preenchida ou se está vazia
    if currency.strip():
        conn.request("GET", "/auto-complete?q="+currency.replace(" ", "-")+"&region=BR", headers=headers)
        res = conn.getresponse()
        data = res.read()
        api_quotes = json.loads(data.decode("utf-8"))['quotes']
        # verifica se o usuário quer procurar somente na B3 ou se quer procurar globalmente utilizando selector na página
        if 'search_selector' in request.GET:
            print(request.GET['search_selector'])
            if request.GET['search_selector'] == '1':
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
    else:
        currency = ''
    return render(request, 'finances/list.html', search_quotes(request, currency))

def my_quotes(request):
    """ Busca por ações com 'search_quotes' através de da aticação da barra de buscas """
    quotes = UserQuotes.objects.filter(user = request.user.id)
    quote_list = ''
    for quote in quotes:
        quote_list += quote.symbol + '%2C'

    print(search_quotes(request, quote_list))
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
        obj, created = UserQuotes.objects.get_or_create(
            symbol=request.POST['symbol'],
            user = user,
            defaults={
                'symbol': request.POST['symbol'],
                'update_interval': request.POST['update_interval'],
                'higher_limit': request.POST['higher_limit'],
                'lower_limit': request.POST['lower_limit'],
                'notification_check': True,
                'user': user
            },
        )

        if not created:
            obj.symbol = request.POST['symbol']
            obj.update_interval = request.POST['update_interval']
            obj.higher_limit = request.POST['higher_limit']
            obj.lower_limit = request.POST['lower_limit']
            obj.notification_check = True
            obj.save()

        return redirect('quote_dashboard', obj.symbol)

def remove_user_quote(request, quote_symbol):
    print(quote_symbol)
    # user = get_object_or_404(User, pk=request.user.id)
    quote = UserQuotes.objects.get(symbol=quote_symbol, user_id=request.user.id)
    print(quote)
    quote.delete()
    return redirect('my_quotes')
