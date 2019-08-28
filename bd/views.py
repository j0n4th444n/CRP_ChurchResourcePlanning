from django.shortcuts import render
from multiprocessing import context
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from bd.models import Member

# Create your views here.

def index(request):
    return render_to_response('bd/index.html')

def gallery(request):
    return render_to_response('bd/gallery.html')

def allmembers(request):
    context = RequestContext(request)
    context_dict = {'members_list': Member.objects.all() }
    return render_to_response('bd/allmembers.html', context_dict, context)
