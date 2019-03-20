from django import forms
from rango.models import Hotel, DogSitter, Dog, DogOwner
from django.contrib.auth.models import User
from phone_field import PhoneField


class DogForm(forms.ModelForm):

    name = forms.CharField(max_length=Dog.max_length, help_text = "Please enter the name of your dog.")
    size = forms.ChoiceField(label="", initial='', widget=forms.Select(), required=True)
    age = forms.IntegerField( help_text="Please enter your dog's age.")
    breed = forms.CharField(max_length=Dog.max_length, help_text = "Please enter your dog's breed(s)")
    special_needs = forms.CharField(max_length=Dog.max_length, help_text = "Please enter any special needs sitters should be aware of.")
    picture = forms.ImageField(required=False)

    class Meta:
        model = Dog
        exclude = ('owner', )
        fields = ('name', 'size', 'age', 'breed', 'special_needs', 'picture', )

class DogOwnerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, help_text = "Please enter your fist name.")
    last_name = forms.CharField(max_length=128, help_text = "Please enter your fist name.")
    email = forms.EmailField(max_length=128, help_text = "Please enter your email.")
    username = forms.CharField(max_length=128, help_text = "Please enter your username.")
    password = forms.CharField(widget=forms.PasswordInput())
    phone_number = PhoneField(blank=True,help_text="Please enter your phone number.")
    city = forms.CharField(max_length=128, help_text = "Please enter your city.")
    picture = forms.ImageField(required=False)

    class Meta:
        model = DogOwner
        fields = ('username', 'first_name', 'last_name', 'email', 'password' ,'phone_number', 'city', 'picture', )

class HotelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, help_text = "Please enter first name.")
    last_name = forms.CharField(max_length=128, help_text = "Please enter last name.")
    email = forms.EmailField(max_length=128, help_text = "Please enter your email.")
    username = forms.CharField(max_length=128, help_text = "Please enter your username.")
    hotel_name = forms.CharField(max_length=128, help_text = "Please enter your hotel's name.")
    address = forms.CharField(max_length=128, help_text = "Please enter the hotel's address.")
    city = forms.CharField(max_length=128, help_text = "Please enter the city of your hotel.")
    picture = forms.ImageField(required=True)
    phone_number = PhoneField(blank=True,help_text="Please enter your phone number.")
    available_rooms = forms.IntegerField()
    description = forms.CharField(max_length = 500)
    price = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Hotel
        fields = ('username', 'hotel_name',  'first_name', 'last_name', 'email', 'password', 'phone_number', 'address', 'city', 'available_rooms', 'description', 'price', 'picture',)


class DogSitterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, help_text = "Please enter your fist name.")
    last_name = forms.CharField(max_length=128, help_text = "Please enter your fist name.")
    email = forms.EmailField(max_length=128, help_text = "Please enter your email.")
    username = forms.CharField(max_length=128, help_text = "Please enter your username.")
    dog_preferences = forms.ChoiceField(label="", initial='', widget=forms.Select(), required=True)
    age = forms.IntegerField(required=False)
    picture = forms.ImageField(required=False)
    bio = forms.CharField(max_length = 500, help_text = "Why do you want to be a dogsitter?")
    price_per_night = forms.IntegerField(required=True, help_text = "Please enter your per night price.")
    availability = forms.CharField(max_length=128)
    phone_number = PhoneField(blank=True,help_text="Please enter your phone number.")
    city = forms.CharField(max_length=128, help_text = "Please enter the city you live in.")#
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = DogSitter
        fields = ('username', 'picture', 'first_name', 'last_name', 'email', 'password', 'dog_preferences', 'age', 'bio', 'price_per_night', 'availability', 'phone_number', 'city', )
