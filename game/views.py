from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect

def game(request):
    return render(request, 'SpaceRocks.html',{})