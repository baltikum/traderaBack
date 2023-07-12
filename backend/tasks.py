

from __future__ import absolute_import,unicode_literals
from celery import shared_task

from .models import Auctions,Searches,Biddings
from bs4 import BeautifulSoup
import requests,json
from os import path
from datetime import datetime,timedelta,timezone
import time




from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import concurrent.futures

import hashlib

from .task_searcher import parse_datetime,add_new_auction,update_auctions,do_search,load_active_searches,insert_auction
from .task_bidder import login_function, load_item, bid_function
          
list_of_booked_biddings = []
taken_biddings = {}
biddings_data_hash = None

active_searches = load_active_searches()
search_data_hash_list = []
found_search_data = {}

def bidding_thread(item, bid):
    try:
        #Start webdriver
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(options=chrome_options)
        time.sleep(3)    
        if not login_function(browser):
            print('LOGIN FAILED')
            result = False
        else:
            result = bid_function(browser,item,bid)
            browser.close()  #quit() ?? stänger den även de utanför tråden ???  
        return f"Bidding was : {result}"
    except:
        browser.close()
        return "Problem in bidding thread, browser closed."




#Called by settings to search for new auctions         
@shared_task
def fetch_and_store_auctions():
    global found_search_data,search_data_hash_list,active_searches
    active_searches = load_active_searches()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = [ executor.submit(do_search,entry.term, entry.category) 
                        for entry in active_searches ] 

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            result = future.result()
            
            if len(search_data_hash_list) == 0 :
                search_data_hash_list = [0] * len(active_searches)
                
            dict_str = str(result).encode('utf-8')
            hash_obj = hashlib.md5(dict_str)
            hash_value = hash_obj.hexdigest()
            if hash_value != search_data_hash_list[i]:
                updates = [ executor.submit(insert_auction, entry) 
                    for entry in result ]
                search_data_hash_list[i] = hash_value
 
    if updates :
        return "Changes were made to DB."
    else:        
        return 'No changes to database.'
        
#Called by settings to set auction booleans.
@shared_task
def set_ending_booleans():
    actives = Auctions.objects.filter(removed=False)
    now = datetime.now(timezone.utc)
    for entry in actives:
        time_diff = entry.end_date - now
        if time_diff < timedelta(days=2):
            entry.ends_soon = True
        if time_diff < timedelta(minutes=-1):
            entry.ended = True
        entry.save()
    return "Ending booleans updated."
           
#checks if < 20min   on any auction with bid, starts bidding thread.     
@shared_task
def check_for_active_bids():
    global list_of_booked_biddings, taken_biddings
    biddings = Biddings.objects.all()
    
    if len(biddings) > 0 :
        now = datetime.now(timezone.utc)
        for entry in biddings:
            time_diff = entry.ends - now
            if time_diff < timedelta(0) :
                Biddings.objects.filter(auction=entry.auction.delete())
                return f"Removed old bidding {entry.auction}"
                
            elif time_diff < timedelta(minutes=20):
                if not taken_biddings.get(entry.auction) :
                    taken_biddings[entry.auction] = entry                
                    res = bidding_thread(entry.auction, entry.highest_bid)
                    if res:
                        taken_biddings.pop(entry.auction)
                        entry.delete()
                        return f"{entry.auction} was bid on with {entry.highest_bid}."
                    else:
                        return f"Failed to bid on {entry.auction}."
                    
                print("Already handeld by another thread.")
            else:
                print(f"Timediff for {entry.auction} longer than 20 minutes.")
        
    else:
        return "No queued biddings."
         
 #   list_of_booked_biddings = sorted(biddings, key=lambda x: x['diff'])  




                

