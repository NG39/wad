from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from phone_field import PhoneField



class DogOwner(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='media', blank=True)
    city = models.CharField(max_length = 128)


    def email(self):
        return self.user.email

    def get_dog_name(self):
        return self.dog.name

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name
    def __str__(self):
	       return self.user.username

class Dog(models.Model):
    max_length = 128
    name = models.CharField(max_length = max_length)
    dog_sizes = (('S', 'Small'), ('M', 'Medium'), ('L', 'Large'))
    size = models.CharField(max_length=1, choices=dog_sizes)
    age = models.IntegerField()
    breed = models.CharField(max_length = max_length)
    special_needs = models.CharField(max_length=max_length)
    picture = models.ImageField(upload_to='dog_images', blank=True) ##CREATE DOG_IMAGES
    owner = models.OneToOneField(DogOwner, on_delete=models.CASCADE,related_name = "owner", null= True,blank=True)


class Hotel(models.Model):
    user = models.OneToOneField(User)
    hotel_name = models.CharField(max_length=128)
    address = models.CharField(max_length = 256)
    city = models.CharField(max_length = 128)
    picture = models.ImageField(upload_to='media', blank=True)
    #phone_number = PhoneField(blank=True, help_text='Contact phone number')
    available_rooms = models.IntegerField()
    description = models.CharField(max_length = 500)
    price = models.IntegerField()

    def __str__(self):
	       return self.user.username

class DogSitter(models.Model):
    user = models.OneToOneField(User)
    dog_size = [('S', 'Small'), ('M', 'Medium'),('L','Large')]
    dog_preferences = models.CharField(max_length=3, choices=dog_size)
    age = models.IntegerField()
    picture = models.ImageField(upload_to='media', blank=True)
    bio = models.CharField(max_length = 500)
    price_per_night = models.IntegerField()
    availability  = models.CharField(max_length=128)
    #phone_number = PhoneField(blank=True, help_text='Contact phone number')
    city = models.CharField(max_length=128)

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name
    def __str__(self):
	       return self.user.username
