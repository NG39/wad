from django import forms
from rango.models import Hotel, DogSitter, Dog, DogOwner
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from phone_field import PhoneField

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128, help_text = "Please enter your fist name.")
    last_name = forms.CharField(max_length=128, help_text = "Please enter your fist name.")
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password')

class DogForm(forms.ModelForm):

    name = forms.CharField(max_length=Dog.max_length, help_text = "Please enter the name of your dog.")
    size = forms.ChoiceField(choices = [('S', 'Small'), ('M', 'Medium'),('L','Large')],label="Dog Preference", initial='', widget=forms.Select(), required=True)
    age = forms.IntegerField( help_text="Please enter your dog's age.")
    breed = forms.CharField(max_length=Dog.max_length, help_text = "Please enter your dog's breed(s)")
    special_needs = forms.CharField(max_length=Dog.max_length, help_text = "Please enter any special needs sitters should be aware of.")
    picture = forms.ImageField(required=False)

    class Meta:
        model = Dog
        exclude = ('owner', )
        fields = ('name', 'size', 'age', 'breed', 'special_needs', 'picture', )

class DogOwnerForm(forms.ModelForm):
    #email = forms.EmailField(max_length=128, help_text = "Please enter your email.")
    #username = forms.CharField(max_length=128, help_text = "Please enter your username.")
    #password = forms.CharField(widget=forms.PasswordInput())
    #phone_number = PhoneField(blank=True, help_text='Contact phone number')
    city = forms.CharField(required=True,max_length=128, help_text = "Please enter your city.")
    picture = forms.ImageField(required=False)

    class Meta:
        model = DogOwner
        exclude = ('user',)
        fields = ( 'city', 'picture', )

class HotelForm(forms.ModelForm):
    #email = forms.EmailField(max_length=128, help_text = "Please enter your email.")
    #username = forms.CharField(max_length=128, help_text = "Please enter your username.")
    hotel_name = forms.CharField(required=False,max_length=128, help_text = "Please enter your hotel's name.")
    address = forms.CharField(required=False,max_length=128, help_text = "Please enter the hotel's address.")
    city = forms.CharField(required=False,max_length=128, help_text = "Please enter the city of your hotel.")
    picture = forms.ImageField(required=False)
    #phone_number = PhoneField(blank=True, help_text='Contact phone number')
    available_rooms = forms.IntegerField(required=False,)
    description = forms.CharField(required=False,max_length = 500)
    price = forms.IntegerField(required=False,)
    #password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Hotel
        exclude = ('user',)
        fields = ('hotel_name', 'address', 'city', 'available_rooms', 'description', 'price', 'picture',)


class DogSitterForm(forms.ModelForm):
    dog_preferences = forms.ChoiceField(choices = [('S', 'Small'), ('M', 'Medium'),('L','Large')],label="Dog Preference", initial='', widget=forms.Select(), required=True)
    age = forms.IntegerField(required=False)
    picture = forms.ImageField(required=False)
    bio = forms.CharField(required=False,max_length = 500, help_text = "Why do you want to be a dogsitter?")
    price_per_night = forms.IntegerField(required=False, help_text = "Please enter your per night price.")
    availability = forms.CharField(required=False,max_length=128)
    #phone_number = PhoneField(blank=True, help_text='Contact phone number')
    city = forms.CharField(required=False,max_length=128, help_text = "Please enter the city you live in.")

    class Meta:
        model = DogSitter
        exclude = ('user',)
        fields = ('picture','dog_preferences', 'age', 'bio', 'price_per_night', 'availability', 'city', )
