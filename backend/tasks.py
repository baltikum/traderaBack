

from __future__ import absolute_import,unicode_literals
from celery import shared_task

from .models import Auctions,Searches
from bs4 import BeautifulSoup
import requests,json
from os import path
from datetime import datetime,timedelta,timezone
import pytz

active_searches = Searches.objects.all()
search_data_hash = None
found_search_data = {}
import hashlib

def parse_datetime(datetime_str):
    try:
        dt = datetime.fromisoformat(datetime_str)
    except ValueError:
        dt = datetime.fromisoformat(datetime_str[:26])
    dt = dt.replace(tzinfo=timezone.utc)
    return dt

def add_new_auction(data):
    start_time = datetime.now()
    end_date = parse_datetime(data['endDate'])
    new_auction = Auctions(
        id = data['itemId'],
        name = data['shortDescription'], 
        description = data['shortDescription'], 
        image_url = data['imageUrl'], 
        item_url = data['itemUrl'], 
        price = data['price'], 
        total_bids = data['totalBids'], 
        seller_alias = data['sellerAlias'],
        search_term = data['search_term'],
        auction_category  = data['auction_category'], 
        end_date = end_date,
        auction_type = True, 
        start_date = start_time,
        new_item = True,
        bidding_on = False,
        ending_soon = False,
        highlighted = False,
        removed = False
    )
    new_auction.save()
    return True, str(new_auction)

def update_auctions(data):
    id_array = list(data.keys())
    existing_auctions = Auctions.objects.filter(id__in=id_array)
    new_ids = set(id_array) - set(existing_auctions.values_list('id', flat=True))
    
    count = 0
    for entry in new_ids:
        res,text = add_new_auction(data[entry])
        count += 1 
    print(f'{count} auctions were inserted.')
    
    count = 0
    for auction in existing_auctions:
        auction.price = data[auction.id]['price']
        auction.total_bids = data[auction.id]['totalBids']
        timezone = pytz.UTC
        now = timezone.localize(datetime.now())
        if (auction.end_date - now) < timedelta(days=2):
            auction.ending_soon = True
        auction.save()
        count += 1   
    print(f'{count} auctions were updated.')



    
    
    '''
        new_auctions = Auctions.objects.filter(id__in=new_ids)
        
        count = 0
        processed_auctions = Auctions.objects.filter(search_term=new.search_term, auction_category=new.auction_category)
        
        my_objects = Auctions.objects.filter(id__in=id_array)
        my_objects = Auctions.objects.exclude(id__in=id_array)
        
        all_processed_auctions = Auctions.objects.filter(search_term=new.search_term, auction_category=new.auction_category)
        
        difference_queryset = queryset1.exclude(id__in=queryset2.values_list('auction_id', flat=True))
        '''
       
def do_search(search_term, auction_category):
    global found_search_data
    default_url = "https://www.tradera.com/search?q="
    category = "&categoryId="
    url = f"{default_url}{search_term}{category}{auction_category}"

    try:
        r = requests.get(url)
        r.raise_for_status()
        s = BeautifulSoup(r.content, features="lxml")
        script = s.find('script', attrs={'id': '__NEXT_DATA__'})
        if script:
            js = json.loads(script.text)
            itemsArray = js['props']['pageProps']['initialState']['discover']['items']
            if itemsArray:
                for entry in itemsArray:
                    entry['search_term'] = search_term
                    entry['auction_category'] = auction_category
                    found_search_data[entry['itemId']] = entry
            
        return True

    except Exception as e:
        print(e)
        return False

def load_active_searches():
    global searches
    searches = Searches.objects.all()
    

           
@shared_task
def fetch_and_store_auctions():
    global found_search_data,search_data_hash,active_searches
    
    load_active_searches()
    
    for entry in active_searches:
        res = do_search(entry.term, entry.category)
        
    dict_str = str(found_search_data).encode('utf-8')
    hash_obj = hashlib.md5(dict_str)
    hash_value = hash_obj.hexdigest()
    
    if hash_value != search_data_hash :
        update_auctions(found_search_data)
        search_data_hash = hash_value
    else:
        print('No changes to database.')

@shared_task
def set_ending_booleans():
    actives = Auctions.objects.filer(removed=False)
    now = datetime.utcnow()
    for entry in actives:
        
        datetime_obj = datetime.fromisoformat(entry.end_date[:-1])
        time_diff = datetime_obj - now
        
        if time_diff < timedelta(days=2):
            entry.ends_soon = True
            entry.save()
            
@shared_task
def place_bid(bid,item,time): 
    print(f'Putting {bid} on {item} at {time}. Time is {datetime.now()}')
        
    