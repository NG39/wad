from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    max_name_length = 128
    name = models.CharField(max_length=max_name_length, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    max_title_length = 128
    last_visit = models.DateTimeField(null=True, blank=True)
    first_visit = models.DateTimeField(default=timezone.now())
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=max_title_length)
    url = models.URLField()
    views = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Pages'

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
