
from .models import Auctions,Searches
import requests,json,pytz
from datetime import timedelta,datetime,timezone
from bs4 import BeautifulSoup


def parse_datetime(datetime_str):
    try:
        dt = datetime.fromisoformat(datetime_str)
    except ValueError:
        dt = datetime.fromisoformat(datetime_str[:26])
    dt = dt.replace(tzinfo=timezone.utc)
    return dt

def add_new_auction(data):
    start_time = parse_datetime(data['startDate'])
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
        removed = False,
        ended = False
    )
    new_auction.save()
    return True, str(new_auction)

def update_auction(existing,entry):
    existing.price = entry['price']
    existing.total_bids = entry['totalBids']
    if ((existing.end_date - datetime.now(timezone.utc)) < timedelta(days=2)):
        existing.ending_soon = True
    elif ((existing.end_date - datetime.now(timezone.utc)) < timedelta(minutes =-1)):
        existing.delete()
    existing.save()
        
def insert_auction(entry):
    existing = Auctions.objects.filter(id=entry['itemId'])
    if existing :
        update_auction(existing,entry)
    else:
        add_new_auction(entry)
    
def update_auctions(data):
    id_array = list(data.keys())
    existing_auctions = Auctions.objects.filter(id__in=id_array)
    all_auctions = Auctions.objects.all()
    ended_auctions = set(all_auctions.values_list('id', flat=True)) - set(id_array) 
    new_ids = set(id_array) - set(existing_auctions.values_list('id', flat=True))
    
    count = 0
    for entry in new_ids:
        res,text = add_new_auction(data[entry])
        count += 1 
    print(f'{count} auctions were inserted.')
    
    count = 0
    for auction in existing_auctions:
        #auction.price = data[auction.id]['price']
        #auction.total_bids = data[auction.id]['totalBids']
        #timezone = pytz.UTC
        #now = timezone.localize(datetime.now())
        #if (auction.end_date - now) < timedelta(days=2):
        #    auction.ending_soon = True
        #auction.save()
        update_auction(auction,data[auction.id])
        count += 1   
    print(f'{count} auctions were updated.')
    
    count = 0
    for auction in ended_auctions:
        Auctions.objects.filter(id=auction).delete()
        count += 1
    print(f'{count} auctions were deleted.')
    
    
    
    
def do_search(search_term, auction_category):
    default_url = "https://www.tradera.com/search?q="
    category = "&categoryId="
    url = f"{default_url}{search_term}{category}{auction_category}"

    try:
        results = []
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
                    results.append(entry)
                    #found_search_data[entry['itemId']] = entry
        return results

    except Exception as e:
        print(e)
        return []

def load_active_searches():
    return Searches.objects.all()
    