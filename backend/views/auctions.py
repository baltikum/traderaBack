
from backend.models import Auctions
from django.http import JsonResponse,HttpResponseBadRequest
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_auction(request, id):
    if request.method == 'GET':
        try:
            auction = Auctions.objects.get(id=id)
            data = {'auction': model_to_dict(auction)}
            return JsonResponse(data, status=200)
        except Auctions.DoesNotExist:
            return JsonResponse({'error': 'Auction not found.'}, status=404)
    else:
        return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=400)
@csrf_exempt    
def get_auctions(request):
    if request.method == 'GET':
        auctions = Auctions.objects.filter(removed=False)
        data = {'auctions': list(auctions.values())}
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=400)
@csrf_exempt    
def delete_auction(request,id):
    if request.method == 'DELETE':
        try:
            Auctions.objects.filter(id=id).delete()
            return JsonResponse({'message': 'Auction deleted successfully.'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('This endpoint only accepts DELETE requests.')
@csrf_exempt    
def show_hide_auction(request,id):
    if request.method == 'PATCH':
        try:
            auction = Auctions.objects.get(id=id)
            auction.removed = not auction.removed
            auction.save()
            return JsonResponse({'message': f'Auction {id} removed value : {auction.removed}.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('This endpoint only accepts PATCH requests.')
@csrf_exempt    
def highlight_auction(request,id):
    if request.method == 'PATCH':
        try:
            auction = Auctions.objects.get(id=id)
            auction.highlighted = not auction.highlighted
            auction.save()
            return JsonResponse({'message': f'Auction {id} highlighted value : {auction.highlighted}'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('This endpoint only accepts PATCH requests.')
@csrf_exempt    
def insert_auction(request):
    if request.method == 'POST':
        try:
            new_auction = Auctions(
                id=request.POST['id'],
                seller_id=request.POST['seller_id'],
                title=request.POST['title'],
                description=request.POST['description'],
                start_price=request.POST['start_price'],
                start_time=request.POST['start_time'],
                end_time=request.POST['end_time'],
                bid_increment=request.POST['bid_increment'],
                auction_category=request.POST['auction_category'],
                search_term=request.POST['search_term']
            )
            new_auction.save()
            return JsonResponse({'message': 'Auction inserted successfully.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('This endpoint only accepts POST requests.')
@csrf_exempt   
def update_auction(request,id):
    if request.method == 'PATCH':
        try:
            auction = Auctions.objects.get(id=id)
            auction.total_bids = request.GET.get('total_bids', auction.total_bids)
            auction.price = request.GET.get('price', auction.price)
            auction.save()
            return JsonResponse({'message': 'Auction updated successfully.'}, status=200)
        except Auctions.DoesNotExist:
            return JsonResponse({'error': 'Auction not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('This endpoint only accepts PUT requests.')