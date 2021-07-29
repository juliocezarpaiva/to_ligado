from apps import finances
from django.shortcuts import redirect, render, get_object_or_404
from background_task.models import Task, CompletedTask
from background_task import background
from django.contrib.auth.models import User
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import finances.views as finances_views

def create_task(request):
    user = get_object_or_404(User, pk=request.user.id)
    Try:    Task.objects.filter(creator=user, locked_at__isnull=True).delete()
    Try:    CompletedTask.objects.filter(creator=user, locked_at__isnull=True).delete()

    return redirect('home')

# @background(schedule=5)
def update_and_notify(request, quote_symbol, higher_limit, lower_limit):
    user = get_object_or_404(User, pk=request.user.id)

    updated_quote = finances_views.get_quote(quote_symbol)['quote']
    if updated_quote:
        quote_dict = {
            'components': updated_quote['components'],
            'shortName': updated_quote['shortName'],
            'longName': updated_quote['longName'],
            'symbol': updated_quote['symbol'],
            'currency': updated_quote['currency'],
            'regularMarketPrice': updated_quote['regularMarketPrice'],
            'regularMarketDayHigh': updated_quote['regularMarketDayHigh'],
            'regularMarketDayRange': updated_quote['regularMarketDayRange'],
            'regularMarketDayLow': updated_quote['regularMarketDayLow'],
            'regularMarketPreviousClose': updated_quote['regularMarketPreviousClose'],
            'targetPriceHigh': updated_quote['targetPriceHigh'],
            'targetPriceLow': updated_quote['targetPriceLow'],
            'targetPriceMean': updated_quote['targetPriceMean'],
            'targetPriceMedian': updated_quote['targetPriceMedian']
        }
        
        quote_price = float(quote_dict['regularMarketPrice'])
        higer_price = float(higher_limit.replace(',','.'))
        lower_price = float(lower_limit.replace(',','.'))

        if quote_price >= higer_price or quote_price <= lower_price:
            subject = 'Alerta de preços da TôLigado!'
            html_message = render_to_string('notify/email.html', quote_dict)
            message = render_to_string('notify/email.html', quote_dict)
            html_message = render_to_string('notify/email.html', quote_dict)
            from_email = 'De <juliocezarpaiva@gmail.com>'
            user.email_user(subject, html_message=html_message, message=message, from_email=from_email)
            return 0
    else:
        return 1

