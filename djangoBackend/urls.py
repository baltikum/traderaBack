"""
URL configuration for djangoBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend.views.bids import get_bidding, get_all_biddings,insert_bid,delete_bid,update_bid
from backend.views.searches import get_searches, get_search, insert_search, delete_search
from backend.views.auctions import get_auction, get_auctions,delete_auction, insert_auction, update_auction,show_hide_auction,highlight_auction




urlpatterns = [
    #path('', get_auction, name='home'),
    
    path('admin/', admin.site.urls),
    
    #Auctions
    path('get_auctions', get_auctions, name='get_auctions'),
    path('get_auction/<int:id>', get_auction, name='get_auction'),
    path('delete_auction/<int:id>', delete_auction, name='delete_auction'),
    path('show_hide_auction/<int:id>', show_hide_auction, name='show_hide_auction'),
    path('highlight_auction/<int:id>', highlight_auction, name='highlight_auction'),
    path('update_auction/<int:id>', update_auction, name='update_auction'),
    path('insert_auction', insert_auction, name='insert_auction'),
    
    
    #Biddings
    path('get_all_biddings', get_all_biddings, name='aboutget_biddings'),
    path('get_bidding/<int:id>', get_bidding, name='get_bidding'),
    path('insert_bid/<int:id>', insert_bid, name='insert_bid'),
    path('delete_bid/<int:id>', delete_bid, name='delete_bid'),
    path('update_bid/<int:id>', update_bid, name='update_bid'),
    
    
    #Searches
    path('get_searches', get_searches, name='get_searches'),
    path('get_search/<str:category>/<str:term>', get_search, name='get_search'),
    path('insert_search/<str:term>/<str:category>', insert_search, name='insert_search'),
    path('delete_search/<int:id>', delete_search, name='delete_search'),
    
]
