from django.shortcuts import render, redirect
from rango.models import Category, Page, UserProfile, User
from rango.forms import CategoryForm, PageForm, UserProfileForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.webhose_search import run_query
from django.utils import timezone


def homepage(request):
    return HttpResponse("Homepage"
                        "<br>"
                        "Rango says hey there partner!"
                        "<br>"
                        "<a href='/rango'>Rango</href>")



def search(request):
    result_list = []
    query = None
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Webhose search function to get the results list!
            result_list = run_query(query)
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


def show_category(request, category_name_slug):
    # Create a context dictionary that we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # Note that filter() returns a list of page objects or an empty list
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        context_dict['query'] = category.name
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    # New code added here to handle a POST request
    # create a default query based on the category name
    # to be shown in the search box

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our search API function to get the results list!
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list
            # Go render the response and return it to the client.

    return render(request, 'rango/category.html', context_dict)


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


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', context={})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


# Updated the function definition

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def track_url(request):
    page_id = None
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.last_visit = timezone.now()

                print(page.views)
                page.save()
                return redirect(page.url)
            except Category.DoesNotExist:
                pass
        return redirect('index')


@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)
    context_dict = {'form': form}
    return render(request, 'rango/profile_registration.html', context_dict)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({
        'website': userprofile.website,
        'picture': userprofile.picture
    })

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if form.is_valid():
            form.save(commit=True)

            return redirect('profile', user.username)

        else:

            print(form.errors)

    return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})


@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()
    return render(request, 'rango/list_profiles.html',
                  {'userprofile_list': userprofile_list})


@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)
        def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)
    return render(request, 'rango/cats.html', {'cats': cat_list})


@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}

    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category,
                                           title=title, url=url)
            pages = Page.objects.filter(category=category).order_by('-views')
            # Adds our results list to the template context under name pages.
            context_dict['pages'] = pages
    return render(request, 'rango/page_list.html', context_dict)








        ##NEW VIEWS######



def get_hotel_list(max_results=0, city_name):#city_name is the city searched for
    hot_list = []
    if starts_with:
        hot_list = Category.objects.filter(city=city_name)
    if max_results > 0:
        if len(hot_list) > max_results:
            hot_list = hot_list[:max_results]
    return hot_list


def get_dogsitter_list(max_results=0, city_name):#city_name is the city searched for
    dogsitter_list = []
    if starts_with:
        dogsitter_list = Category.objects.filter(city=city_name)
    if max_results > 0:
        if len(dogsitter_list) > max_results:
            dogsitter_list = dogsitter_list[:max_results]
    return dogsitter_list



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


def add_dog:





































def hotelprofile1(request, username):
    try:
        hotelname = Hotel.objects.get(user=user);
    except:
        return redirect('') ###HOTEL SEARCH PAGE

    hotelprofile = Hotel.objects.get_or_create(hotelname=hotelname)[0]
    form = Hotelprofileform({
        'username': hotelprofile.user,##cahngr it
        'address' : hotelprofile.address,
        'city' : hotelprofile.city,
        'picture' : hotelprofile.picture,
        'phone number' : hotelprofile.phone_number,
        'avaialable rooms' : hotelprofile.available_rooms,
        'description' : hotelprofile.description,
        'price' : hotelprofile.price})
    if request.method == 'POST':
        form = Hotelprofileform(request.POST, request.FILES, instance = hotelprofile)

        if form.is_valid():
            form.save(commit=True)

            return redirect('hotelprofile1', hotelname.user)
        else:
            print(form.errors)

    return render(request, 'homepage.html', {'hotelprofile' : hotelprofile, 'selectedhotel': hotelname, 'form': form})##edit


def help(): ##to be continued





    
    


def hotel_owner_profile(request, username):   ##NEEDS AND UPDATE OPTION
    try:
        hotelname = Hotel.objects.get(user=user);
    except:
        return redirect('') ###HOTEL SEARCH PAGE

    hotelprofile = Hotel.objects.get_or_create(hotelname=hotelname)[0]
    form = Hotelprofileform({
        'username': hotelprofile.user,##change it
        'address' : hotelprofile.address,
        'city' : hotelprofile.city,
        'picture' : hotelprofile.picture,
        'phone number' : hotelprofile.phone_number,
        'avaialable rooms' : hotelprofile.available_rooms,
        'description' : hotelprofile.description,
        'price' : hotelprofile.price})
    if request.method == 'GET':
        form = Hotelprofileform(request.GET, request.FILES, instance = hotelprofile)

        if form.is_valid():
            form.save(commit=True)

            return redirect('hotelprofile1', hotelname.user)
        else:
            print(form.errors)

    return render(request, 'rango/ogprofile.html', {'hotelprofile' : hotelprofile, 'selectedhotel': hotelname, 'form': form})
    

    
def Dogsitterprofile():
    try:
        dogsittername = DogSitter.objects.get(user=user);
    except:
        return redirect('') ###HOTEL SEARCH PAGE

    dogsitterprofile = DogSitter.objects.get_or_create(dogsittername=dogsittername)[0]
    form = Dogsitterprofileform({
        'username': dogsitterprofile.user,##change it
        'size' :  dogsitterprofile.dog_size,
        'age': dogsitterprofile.age,
        'picture': dogsitterprofile.picture,
        'bio':dogsitterprofile.bio,
        'price/night': dogsitterprofile.price_per_night,
        'availability': dogsitterprofile.availability,
        'phone_number': dogsitterprofile.phone_number,
        'city': dogsitterprofile.city,
        
    if request.method == 'POST':
        form = Dogsitterprofileform(request.POST, request.FILES, instance = dogsitterprofile)

        if form.is_valid():
            form.save(commit=True)

            return redirect('hotelprofile1', hotelname.user)
        else:
            print(form.errors)

    return render(request, 'rango/profile.html', {'hotelprofile' : hotelprofile, 'selectedhotel': hotelname, 'form': form})




def hotelsearch():
    # Create a context dictionary that we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        hotel = Hotel.objects.get(slug=city_name_slug)
        # Retrieve all of the associated pages.
        # Note that filter() returns a list of page objects or an empty list
        hotels = Hotel.objects.filter(hotel=hotel)
        # Adds our results list to the template context under name pages.
        context_dict['hotels'] = hotels
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['hotel'] = hotel
        context_dict['query'] = hotel.name
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    # New code added here to handle a POST request
    # create a default query based on the category name
    # to be shown in the search box

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our search API function to get the results list!
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list
            # Go render the response and return it to the client.

    return render(request, 'rango/category.html', context_dict)

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





