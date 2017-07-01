from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .forms import CreateContact


@login_required
def contact(request):
    confirm = []
    form = CreateContact(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm.append(
                'Your message has been successfully sent!\nThank you!')
            form = CreateContact(None)
    return render(request, 'contact/contact.html',
                  {'form': form,
                   'confirm': confirm},
                  )