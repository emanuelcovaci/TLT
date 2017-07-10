from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .forms import CreateContact
from django.core.mail import send_mail
from django.conf import settings


def contact(request):
    confirm = []
    form = CreateContact(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            subject = "Informatii"
            text = form.cleaned_data['message']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email_form = form.cleaned_data['email']
            messages = "Multumim pentru ca ne-ati contactat!\nMai jos aveti informatiile competate " \
                       "de dvs. in formul de contact\nPrenume: %s\n" \
                       "Nume %s\nEmail: %s\n Mesaj: \n%s\nO sa raspundem in cel mai" \
                       " scurt timp!\nO zi buna !"%(first_name,last_name,email_form,text)
            from_email = settings.EMAIL_HOST_USER
            to_list = [email_form, settings.EMAIL_HOST_USER]
            send_mail(subject, messages, from_email, to_list, fail_silently=True)
            form.save()
            confirm.append(
                'Am primit mesajul tau!\nMultumim!')
            form = CreateContact(None)
    return render(request, 'contact/contact.html',
                  {'form': form,
                   'confirm': confirm},
                  )
