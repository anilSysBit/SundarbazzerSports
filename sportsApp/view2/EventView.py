from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse,render,redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.db import IntegrityError
from django.conf import settings


def index(request):
    if request.user:
        return render(request,'./event/event_home.html')
    return redirect('login')


def edit_profile_view(request):
    if request.method == 'POST':
        return render('')
