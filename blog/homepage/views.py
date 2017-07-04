from django.shortcuts import render
from activity.models import Activity


# Create your views here.
def index(request):
    activities = Activity.objects.all()[:3]
    return render(request, 'homepage/index.html', {
        'activities': activities
    })


def about(request):
    return render(request, 'homepage/about.html')
