from django.shortcuts import render, redirect
from rango.models import DogOwnerForm, DogForm, HotelForm, DogSitterForm, User
from rango.forms import CategoryForm, PageForm, UserProfileForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.webhose_search import run_query
from django.utils import timezone



def add_dog(request):
    form = AddDogForm()
    
    if request.method == 'POST':
        form = AddDogForm(request.POST)
        
        if form.is_valid():

            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_dog.html', {'form':form})


    


































