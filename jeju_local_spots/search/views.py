from django.shortcuts import render
from django.db.models import Q
from spots.models import Spot
from events.models import Event

def unified_search(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    
    spots = []
    events = []
    
    if query:
        if search_type == 'spots' or search_type == 'all':
            spots = Spot.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(address__icontains=query) | 
                Q(category__icontains=query)
            )
        
        if search_type == 'events' or search_type == 'all':
            events = Event.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(location__icontains=query) | 
                Q(event_type__icontains=query)
            )
    
    context = {
        'query': query,
        'search_type': search_type,
        'spots': spots,
        'events': events,
        'total_results': len(spots) + len(events)
    }
    
    return render(request, 'search/search_results.html', context)
