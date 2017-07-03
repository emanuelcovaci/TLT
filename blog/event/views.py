from blog import settings

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http.response import HttpResponseForbidden
from django.shortcuts import render

from models import Event


def event_all(request):
    events = Event.objects.all()
    paginator = Paginator(events, 4)

    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    return render(request, 'event/all_events.html', {
        'events': events,
    })


def event_detail(request, slug):
    articol = list(Event.objects.values('name', 'text', 'date', 'file',
                                        'author',
                                         'address',
                                        'geolocation',
                                        'location',
                                        'slug').filter(slug=slug))
    other_event = Event.objects.all()[:4]
    return render(request, 'event/event.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'name': articol[0].get('name'),
        'text': articol[0].get('text'),
        'location': articol[0].get('address'),
        'geolocation': articol[0].get('geolocation'),
        'author': articol[0].get('author'),
        'date': articol[0].get('date'),
        'other_event': other_event,
        'thumbnail': "/media/" + articol[0].get('file'),

    })
