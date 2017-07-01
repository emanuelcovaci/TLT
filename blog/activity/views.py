from django.shortcuts import render


# Create your views here.
def activity(request):
    return render(request, 'activity/activity.html')


def post(request):
    return render(request, 'activity/post.html')
