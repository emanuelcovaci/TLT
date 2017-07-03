import json
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.http.response import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views.static import serve

from models import Post
from forms import PostFormSet
import blog.settings



def files_filter(request):
    return JsonResponse({'results': list(Post.objects.filter(Q(name__contains=request.GET["query"]) |
                                                             Q(author__first_name__contains=request.GET["query"]) |
                                                             Q(author__last_name__contains=request.GET["query"]),
                                                             location="articolFiles")
                                         .values('name', 'author','file'))})


@staff_member_required
def add_multiple_files(request):
    if request.method == "POST":
        formset = PostFormSet(data=request.POST or None, files=request.FILES or None)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.author = request.user
                instance.save()
            formset.save_m2m()
            return redirect("/admin/file/post/")
        else:
            response = HttpResponse(json.dumps({"errors": formset.errors}),
                                    content_type='application/json')
            response.status_code = 400
            return response
    else:
        return HttpResponseForbidden()


@staff_member_required
def page_preview(request):
    if request.method == "GET":
        return HttpResponse(
            "<head><title>" + "{0}" + '</title><link rel="stylesheet" type="text/css" '
                                      'href="/static/prism/prism.css"><script '
                                      'src="/static/prism/prism.js"></script></head><body>' + "{0}<br>" +
            request.user.get_full_name() + "<br>{1}" + "</body>")
    else:
        return HttpResponseForbidden()


@staff_member_required
def download_interior_file(request, slug):
    given_file = get_object_or_404(Post, slug=slug)
    path = given_file.file.path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def exterior_files(request, location, path):
    if location is not "articolFiles":
        return serve(request, os.path.join("documents", location, path), document_root=blog.settings.MEDIA_ROOT)
