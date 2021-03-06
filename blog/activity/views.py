from django.shortcuts import render
from .models import Activity
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from gallery.models import Gallery,GalleryPhoto


# Create your views here.
def activity(request):
    all_activity = Activity.objects.all()
    paginator = Paginator(all_activity, 3)

    page = request.GET.get('page')
    try:
        all_activity = paginator.page(page)
    except PageNotAnInteger:
        all_activity = paginator.page(1)
    except EmptyPage:
        all_activity = paginator.page(paginator.num_pages)

    return render(request, 'activity/activity.html', {
        'all_activity': all_activity,
    })


def post(request,slug):
    articol = list(Activity.objects.values('name', 'text', 'author', 'file', 'date',
                                       'slug','album',).filter(slug=slug))
    instance = Gallery.objects.get(id=articol[0].get('album'))
    photos = GalleryPhoto.objects.filter(gallery=instance).extra(
        select={'order': 'CAST(name AS INTEGER)'}
    ).order_by('order')
    print photos
    return render(request, 'activity/post.html',{
        'name': articol[0].get('name'),
        'text': articol[0].get('text'),
        'author': articol[0].get('author'),
        'date': articol[0].get('date'),
        'thumbnail': "/media/" + articol[0].get('file'),
        'photos':photos,
    })
