
from backend.models import Searches
from django.http import JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_searches(request):
    if request.method == 'GET':
        searches = Searches.objects.all()
        search_list = []
        for search in searches:
            search_list.append({
                'id': search.id,
                'term': search.term,
                'category': search.category,
                'average_price': search.average_price,
                'highest_price': search.highest_price,
                'lowest_price': search.lowest_price
            })
        return JsonResponse(search_list, safe=False, status=200)
    else:
        return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=500)
@csrf_exempt  
def get_search(request, id):
    if request.method == 'GET':
        try:
            search = Searches.objects.get(id=id)
            search_data = {
                'id': search.id,
                'term': search.term,
                'category': search.category,
                'average_price': search.average_price,
                'highest_price': search.highest_price,
                'lowest_price': search.lowest_price
            }
            return JsonResponse(search_data, safe=False,status=200)
        except Searches.DoesNotExist:
            return JsonResponse({'error': 'Search does not exist.'}, status=404)
    else:
        return JsonResponse({'error': 'This endpoint only accepts GET requests.'}, status=405)
@csrf_exempt
def insert_search(request,term,category):
    if request.method == 'POST':
        try:
            new_search = Searches(
                term=term, 
                category=category, 
                average_price=None, 
                highest_price=None, 
                lowest_price=None)
            new_search.save()
            return JsonResponse({'message': 'Search inserted successfully.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('This endpoint only accepts POST requests.')
@csrf_exempt    
def delete_search(request,id):
    if request.method == 'DELETE':
            try:
                Searches.objects.filter(id=id).delete()
                return JsonResponse({'message': 'Search deleted successfully.'}, status=204)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('This endpoint only accepts DELETE requests.',status=400)
