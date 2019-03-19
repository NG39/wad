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
    return HttpResponse("<a href='/rango'>Welcome to AirbnBark</href>")


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
    return render(request, 'rango/search.html', {'result_list': result_list, 'search_query': query})





def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    context_dict['last_visit'] = request.session['last_visit'].split('.')[0]

    response = render(request, 'rango/index.html', context=context_dict)
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
        context_dict['query'] = dogsitter.fist_name + " " +dogsitter.last_name

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
@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    ctx = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered}

    return render(request, 'rango/register.html', context=ctx)



def get_hotel_reservation_dets(request, city_name):
    hot = Hotel.objects.get(city=city_name)
    context = {
        ##what we want to be displayed##
        'name': hot.name,
        'description': hot.description,
    }
    return render(request, "wad/hot_detail.html", context)


def get_dogsitter_reservation_dets(request, city_name):
    sitter = DogSitter.objects.get(city=city_name)
    context = {
        ##what we want to be displayed##
        'name': sitter.name,
        'description': sitter.description,
    }
    return render(request, "wad/sitter_detail.html", context)



def register_hotel(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        hotel_form = HotelForm(data=request.POST)

        # If the two forms are valid...
        if hotel_form.is_valid():
            # Save the user's form data to the database.
            hotel_user = hotel_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            hotel_user.set_password(user.password)
            hotel_user.save()


            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
             #put it in the UserProfile model.
            if 'picture' in request.FILES:
                hotel_user.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            hotel_user.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(hotel_form.errors)

    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        hotel_form = HotelForm()


# Render the template depending on the context.
    return render(request,
        'rango/register_hotel.html',
        {'hotel_form': hotel_form,
        'registered': registered})



def register_sitter(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        sitter_form = SitterForm(data=request.POST)

        # If the two forms are valid...
        if sitter_form.is_valid():
            # Save the user's form data to the database.
            sitter_user = sitter_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            sitter_user.set_password(user.password)
            sitter_user.save()


            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
             #put it in the UserProfile model.
            if 'picture' in request.FILES:
                sitter_user.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            sitter_user.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(sitter_form.errors)

    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        sitter_form = SitterForm()


# Render the template depending on the context.
    return render(request,
        'rango/register_sitter.html',
        {'sitter_form': sitter_form,
        'registered': registered})

def register_dog_owner(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        dog_owner_form = DogOwnerForm(data=request.POST)

        # If the two forms are valid...
        if dog_owner_form.is_valid():
            # Save the user's form data to the database.
            dog_owner_user = dog_owner_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            dog_owner_user.set_password(user.password)
            dog_owner_user.save()


            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
             #put it in the UserProfile model.
            if 'picture' in request.FILES:
                dog_owner_user.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            dog_owner_user.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(dog_owner_form.errors)

    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        dog_owner_form = DogOwnerForm()


# Render the template depending on the context.
    return render(request,
        'rango/register_dog_owner.html',
        {'dog_owner_form': dog_owner_form,
        'registered': registered})


def get_hotel_profile(request, city_name):
    hot = Hotel.objects.get(city=city_name)
    context = {
        ##what we want to be displayed##
        'name': hot.name,
        'description': hot.description,
    }
    return render(request, "wad/hot_detail.html", context)


def get_dogsitter_profile(request, city_name):
    sitter = DogSitter.objects.get(city=city_name)
    context = {
        ##what we want to be displayed##
        'name': sitter.name,
        'description': sitter.description,
    }
    return render(request, "wad/sitter_detail.html", context)


def get_dog_owner_profile(request):
    owner = DogOwner.objects.getall()
    context = {
        ##what we want to be displayed##
        'name': owner.name,
        'description': owner.description,
    }
    return render(request, "wad/dog_owner_detail.html", context)
