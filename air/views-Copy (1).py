






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



def get_hotel_reservation_dets(request, hotelname): ##
    hot = Hotel.objects.get(hotel_name=hotelname)
    context = {
        ##what we want to be displayed##
        'name': hot.hotel_name,
        'picture': hot.picture,
        'description': hot.description,
        'phone number': hot.phone_number,
        'price': hot.price,
        'address': hot.address,
        'picture': picture,
        'available rooms': hot.available_rooms,

    }
    return render(request, "wad/hot_res_details.html", context)






def get_dogsitter_reservation_dets(request, sittername):
    sitter = DogSitter.objects.get(sitter_name=sittername)
    context = {
        ##what we want to be displayed##
        'name': sitter.username,
        'picture': sitter.picture,
        'description': sitter.bio,
        'price per night': sitter.price_per_night,
        'dog preferences': sitter.dog_preferences,
        'availability': sitter.availability,
        'phone number': sitter.phone_number,
        'city': sitter.city,
    }
    return render(request, "wad/sitter_res_details.html", context)



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


def get_hotel_profile(request, hotel_name):
    hot = Hotel.objects.get(name=hotel_name)
    context = {
        ##what we want to be displayed##
        'name': hot.name,
        'description': hot.description,
    }
    return render(request, "wad/hot_profilepage.html", context)


def get_dogsitter_profile(request, city_name):
    sitter = DogSitter.objects.get(city=city_name)
    context = {
        ##what we want to be displayed##
        'name': sitter.name,
        'description': sitter.description,
    }
    return render(request, "wad/sitter_profilepage.html", context)


def get_dog_owner_profile(request):
    owner = DogOwner.objects.getall()
    context = {
        ##what we want to be displayed##
        'name': owner.name,
        'description': owner.description,
    }
    return render(request, "wad/dog_owner_detail.html", context)


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


    


































