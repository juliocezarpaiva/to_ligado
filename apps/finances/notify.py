from django.shortcuts import get_object_or_404
from background_task.models import Task
from background_task import background
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import finances.views as finances_views

def delete_tasks(verbose_name):
    tasks = Task.objects.filter(verbose_name=verbose_name)
    if tasks:
        for task in tasks:
            task.delete()
    return 0

def create_task(request, quote_symbol, higher_limit, lower_limit, update_interval):
    user = get_object_or_404(User, pk=request.user.id)
    verbose_name="quote-"+quote_symbol+"-user-"+str(request.user.id)

    delete_tasks(verbose_name)
    update_and_notify(request.user.id, quote_symbol, higher_limit, lower_limit, verbose_name=verbose_name, creator=user, repeat=int(update_interval)*60, repeat_until=None)
    
    return 0

@background(schedule=5)
def update_and_notify(user_id, quote_symbol, higher_limit, lower_limit):
    user = get_object_or_404(User, pk=user_id)
    updated_quote = finances_views.get_quote(quote_symbol)['quote']

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
            'targetPriceMedian': ''
        }
        for key in quote_dict:
            if updated_quote[key]:
                quote_dict[key] = updated_quote[key]
            else:
                quote_dict[key] = '-'
        
        if quote_dict['regularMarketPrice'] != '-':
            quote_price = float(quote_dict['regularMarketPrice'])
        else:
            quote_price = 0
        higher_price = float(higher_limit)
        lower_price = float(lower_limit)

        print(quote_price, higher_price, lower_price)

        if quote_price >= higher_price or quote_price <= lower_price:
            subject = 'Alerta de preços da TôLigado!'
            html_message = render_to_string('notify/email.html', quote_dict)
            message = render_to_string('notify/email.html', quote_dict)
            html_message = render_to_string('notify/email.html', quote_dict)
            from_email = 'De Julio do TôLigado! <juliocezarpaiva@gmail.com>'
            user.email_user(subject, html_message=html_message, message=message, from_email=from_email)
            return 0
    else:
        return 1