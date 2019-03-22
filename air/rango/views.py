from django.shortcuts import render, redirect
from rango.models import *
from rango.forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.webhose_search import run_query
from django.utils import timezone


def homepage(request):
    return render(request, 'rango/index.html', {})


def get_hotel_list(city_name,max_results=0,):#city_name is the city searched for
    hot_list = []
    try:
        hot_list = Hotel.objects.filter(city=city_name)
    except:
        hot_list = []
        if max_results > 0:
                if len(hot_list) > max_results:
                        hot_list = hot_list[:max_results]
    return hot_list


def get_dogsitter_list(city_name,max_results=0,):#city_name is the city searched for
    try:
        dogsitter_list = DogSitter.objects.filter(city=city_name)
    except:
        dogsitter_list = []
    if max_results > 0:
        if len(dogsitter_list) > max_results:
            dogsitter_list = dogsitter_list[:max_results]
    return dogsitter_list

def search(request):
    result_list = []
    query = None
    query = request.GET['query'].strip()
    choice = request.GET['choice'] #will get value of button
    city_name = query
    if query:
        if choice=="hotels":
            result_list = get_hotel_list(city_name)
        if choice=="dogsitters":
            result_list = get_dogsitter_list(city_name)
    return render(request, 'rango/search_results.html', {'result_list': result_list, 'search':choice, 'query': query})





def index(request):

    response = render(request, 'rango/index.html', context={})
    return response


def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED")
        request.session.delete_test_cookie()
    context_dict = {'author': "2086380A"}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)




def show_hotel(request, hotel_name_slug):

    context_dict = {}
    try:

        hotel = Hotel.objects.get(slug=hotel_name_slug)

        context_dict['hotel'] = hotel
        context_dict['query'] = hotel.name

    except Hotel.DoesNotExist:
        context_dict['hotel'] = None


    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:

            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list


    return render(request, 'rango/hotel.html', context_dict)

def show_dogsitter(request, dogsitter_name_slug):

    context_dict = {}
    try:
        dogsitter = DogSitter.objects.get(slug=dogsitter_name_slug)
        context_dict['dogsitter'] = dogsitter
        context_dict['query'] = dogsitter.first_name + " " +dogsitter.last_name

    except DogSitter.DoesNotExist:
        context_dict['dogsitter'] = None

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list

    return render(request, 'rango/dogsitter.html', context_dict)



def get_hotel_reservation_dets(request, city_name):
    hot = Hotel.objects.get(city=city_name)
    context = {
        ##what we want to be displayed##
        'name': hot.name,
        'description': hot.description,
    }
    return render(request, "rango/hot_detail.html", context)


def get_dogsitter_reservation_dets(request, city_name):
    sitter = DogSitter.objects.get(city=city_name)
    context = {
        ##what we want to be displayed##
        'name': sitter.name,
        'description': sitter.description,
    }
    return render(request, "rango/sitter_detail.html", context)



def register_hotel(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        hotel_form = HotelForm(data=request.POST)

        if user_form.is_valid() and hotel_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            hotel_user = hotel_form.save(commit=False)
            hotel_user.user = user


            if 'picture' in request.FILES:
                hotel_user.picture = request.FILES['picture']

            hotel_user.save()
            registered = True
        else:

            print(user_form.errors,hotel_form.errors)

    else:
        user_form = UserForm()
        hotel_form = HotelForm()
    ctx = {
        'user_form': user_form,
        'hotel_form':hotel_form,
        'registered': registered}

# Render the template depending on the context.
    return render(request,
        'registration/register_hotel.html',
        context=ctx)


def register_sitter(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        sitter_form = DogSitterForm(data=request.POST)

        if user_form.is_valid() and sitter_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            sitter_user = sitter_form.save(commit=False)
            sitter_user.user = user


            if 'picture' in request.FILES:
                sitter_user.picture = request.FILES['picture']

            sitter_user.save()
            registered = True
        else:

            print(user_form.errors,sitter_form.errors)

    else:
        user_form = UserForm()
        sitter_form = DogSitterForm()
    ctx = {
        'user_form': user_form,
        'sitter_form':sitter_form,
        'registered': registered}

# Render the template depending on the context.
    return render(request,
        'registration/register_sitter.html',
        context=ctx)


def register_dog_owner(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        dog_owner_form = DogOwnerForm(data=request.POST)

        if user_form.is_valid() and dog_owner_form.is_valid():
            user, was_created = User.objects.get_or_create(**user_form.cleaned_data)
            user.set_password(user.password)
            user.save()
            dog_owner_user = dog_owner_form.save(commit=False)
            dog_owner_user.user = user

            if 'picture' in request.FILES:
                dog_owner_user.picture = request.FILES['picture']

            dog_owner_user.save()
            registered = True
        else:

            print(user_form.errors,dog_owner_form.errors)

    else:
        user_form = UserForm()
        dog_owner_form = DogOwnerForm()
    ctx = {
        'user_form': user_form,
        'dog_owner_form':dog_owner_form,
        'registered': registered}

# Render the template depending on the context.
    return render(request,
        'registration/register_dog_owner.html',
        context=ctx)


''' # FIXME:  on click  not with city name arg
def get_hotel_profile(request, city_name):
    hot = Hotel.objects.get(city=city_name)
    context = {
        ##what we want to be displayed##
        'name': hot.name,
        'description': hot.description,
    }
    return render(request, "rango/hot_detail.html", context)

 # FIXME:  on click  not with city name arg get profile page if u are a dogsitter
def get_dogsitter_profile(request, city_name):
    sitter = DogSitter.objects.get(city=city_name)
    context = {
        ##what we want to be displayed##
        'name': sitter.name,
        'description': sitter.description,
    }
    return render(request, "rango/sitter_detail.html", context)

 # FIXME:  get the profilepage when u are a dog owner
def get_dog_owner_profile(request):
    owner = DogOwner.objects.getall()
    context = {
        ##what we want to be displayed##
        'name': owner.name,
        'description': owner.description,
    }
    return render(request, "rango/dog_owner_detail.html", context)
'''
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


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    error = None
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                error = "Your Rango account is disabled."

        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            error = "Invalid login details supplied."

    return render(request, 'rango/login.html', {'error': error})

# Render the template depending on the context.
    return render(request,
        'registration/register_dog_owner.html',
        {'dog_owner_form': dog_owner_form,
        'registered': registered})

@login_required
def user_deactivate(request, username):
    context_dict = {}

    try:
        user = User.objects.get(username=username)
        user.is_active = False
        user.save()
        context_dict['result'] = 'The user has been disabled.'
    except User.DoesNotExist:
        context['result'] = 'User does not exist.'
    except Exception as e:
        context['error'] = e.message

    return render(request, 'registration/deactivate.html', context=context_dict)







def get_dog_owner(user):
    DogOwner.objects.get(user=user)
    userprofile = DogOwner.objects.get_or_create(user=user)[0]
    fields = (
    "Name:\n"+ userprofile.user.first_name,
    " " + userprofile.user.last_name,
    "\nCity:\n"+userprofile.city)
    try:
        userprofile.get_dog_name()
        doginfo = (
        "Name:\n"+userprofile.name,
        "\nBreed:\n"+userprofile.breed,
        "\nSize:\n"+str(userprofile.size),
        "\nAge:\n"+str(userprofile.age),
        "\nSpecial needs:\n"+userprofile.special_needs

        )
    except:
        doginfo = None

    return (userprofile, fields, doginfo )


def get_hotel(user):
    Hotel.objects.get(user=user)
    userprofile = Hotel.objects.get_or_create(user=user)[0]
    title = userprofile.hotel_name
    fields = (
    "Description:\n"+userprofile.description,
    "Adress:\n"+userprofile.address,
    "City:\n"+userprofile.city,
    "Number of available rooms:\n"+str(userprofile.available_rooms),
    "Price in pounds:\n"+str(userprofile.price_pounds),)
    return (userprofile, fields,title)

def get_dog_sitter(user):
    DogSitter.objects.get(user=user)
    userprofile = DogSitter.objects.get_or_create(user=user)[0]
    fields=("Name:\n"+userprofile.first_name(),
    " " +userprofile.last_name(),
    "\nAge:\n"+str(userprofile.age),
    "\nBio:\n"+ userprofile.bio,
    "\nCity:\n"+userprofile.city,
    "\nAvailability:\n"+ userprofile.availability,
    "\nPrice per night per dog:\n"+ str(userprofile.price_per_night))
    return (userprofile,fields)


@login_required
def profile(request, username):
    form=None
    ct= {}
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    title = user.first_name + " " + user.last_name
    try:
        userprofile,fields,doginfo = get_dog_owner(user)
        type = "dog_owner"
        print(type)
    except:
        try:
            userprofile,fields = get_dog_sitter(user)
            type = "dog_sitter"
        except:
            try:
                userprofile,fields,title = get_hotel(user)
                type = "hotel"
            except:
                pass
    #type,userprofile,fields,doginfo = get_dog_owner(user)
    if type=="dog_owner":
        form = DogOwnerForm(request.POST, request.FILES, instance=userprofile)

    elif type=="hotel":
        form = HotelForm(request.POST, request.FILES, instance=userprofile)
    else:
        form = DogSitterForm(request.POST, request.FILES, instance=userprofile)

    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    return render(request, 'rango/profile.html', {"type":type, "fields":fields, 'title':title,
            'userprofile': userprofile, 'selecteduser': user, 'form': form})
