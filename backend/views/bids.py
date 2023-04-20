
from backend.models import Biddings
from django.http import JsonResponse,HttpResponseBadRequest
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from backend.tasks import place_bid

@csrf_exempt
def get_bidding(request, id):
    if request.method == 'GET':
        try:
            bidding = Biddings.objects.get(auction_id=id)
            data = {'bidding': model_to_dict(bidding)}
            return JsonResponse(data, status=200)
        except Biddings.DoesNotExist:
            return JsonResponse({'error': 'Bidding not found.'}, status=404)
    else:
        return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=400)
@csrf_exempt    
def get_all_biddings(request):
    if request.method == 'GET':
        biddings = Biddings.objects.all()
        data = {'biddings': list(biddings.values())}
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=400)
@csrf_exempt    
def insert_bid(request):
    if request.method == 'POST':
        try:
            auction_id = request.POST.get('auction_id')
            highest_bid = request.POST.get('highest_bid')
            ends = request.POST.get('ends')
            
            new_bid = Biddings(
                auction_id=auction_id,
                highest_bid=highest_bid,
                ends=ends
            )
            
            new_bid.save()
            
            booking = place_bid.apply_async(args=[highest_bid,auction_id,ends], eta=ends)
            booking.revoke()
            
            return JsonResponse({'message': 'Bid inserted successfully.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('This endpoint only accepts POST requests.',status=400)
@csrf_exempt    
def delete_bid(request,id):
    if request.method == 'DELETE':
        try:
            Biddings.objects.filter(id=id).delete()
            return JsonResponse({'message': 'Bid deleted successfully.'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('This endpoint only accepts DELETE requests.',status=400)
@csrf_exempt      
def update_bid(request):
    if request.method == 'PATCH':
        try:
            auction_id = request.POST.get('auction_id')
            highest_bid = request.POST.get('highest_bid')
            ends = request.POST.get('ends')

            Biddings.objects.filter(auction_id=auction_id).update(
                highest_bid=highest_bid,
                ends=ends
            )
            return JsonResponse({'message': 'Bid updated successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('This endpoint only accepts PATCH requests.')