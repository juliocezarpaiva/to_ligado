from django.urls import path
from . import views

urlpatterns = [
    # path('checa_api', views.checa_api, name='checa_api'),
    path('search', views.search, name='search'),
    path('quote_dashboard/<str:quote_symbol>', views.quote_dashboard, name='quote_dashboard'),
    path('my_quotes', views.my_quotes, name='my_quotes'),
    path('create_user_quote', views.create_user_quote, name='create_user_quote'),
    path('remove_user_quote/<str:quote_symbol>', views.remove_user_quote, name='remove_user_quote'),
    path('market', views.market, name='market'),
]