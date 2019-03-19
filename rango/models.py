from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator


class DogOwner(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    phone_number = models.IntegerField(validators=[MaxLengthValidator(11),MinLengthValidator(11)])
    city = models.CharField(max_length=128)
    dog = models.ForeignKey(Dog)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
		self.slug = slugify(self.username)
		super(DogOwner, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Hotel(models.Model):
    user = models.OneToOneField(User)
    hotel_name = models.CharField(max_length=128)
    address = models.CharField(max_length = 256)
    city = models.CharField(max_length = 128)
    picture = models.ImageField(upload_to='hotel_images', blank=True)
    phone_number = models.IntegerField(validators=[MaxLengthValidator(11),MinLengthValidator(11)])
    available_rooms = models.Integerfield(default=0)
    description = models.CharField(max_length = 500)
    price = models.IntegerField()
    slug = models.SlugField()

    def save(self, *args, **kwargs):
		self.slug = slugify(self.username)
		super(Hotel, self).save(*args, **kwargs)

    def __str__(self):
		return self.username

class DogSitterP(models.Model):
    user = models.OneToOneField(User)
    dog_size = (('S', 'Small'), ('M', 'Medium'),('L','Large'))
    dog_preferences = models.CharField(max_length=3, choices=dog_size)
    age = models.IntegerField()
    picture = models.ImageField(upload_to='Sitter_images', blank=True)
    bio = models.CharField(max_length = 500)
    price_per_night = models.IntegerField()
    availablity = models.CharField(max_length=128)
    phone_number = models.IntegerField(validators=[MaxLengthValidator(11),MinLengthValidator(11)])
    city = models.CharField(max_length=128)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
		self.slug = slugify(self.username)
		super(DogSitter, self).save(*args, **kwargs)

    def __str__(self):
		return self.username

class Dog(models.Model):
    max_length = 128
    name = models.CharField(max_length = max_length)
    dog_sizes = (('S', 'Small'), ('M', 'Medium'), ('L', 'Large'))
    size = models.CharField(max_length=1, choices=dog_sizes)
    age = models.IntegerField(max_length=2)
    breed = models.CharField(max_length = max_length)
    special_needs = models.CharField(max_length=max_length)
    picture = models.ImageField(upload_to='dog_images', blank=True) ##CREATE DOG_IMAGES
    owner = models.ForeignKey(DogOwner)