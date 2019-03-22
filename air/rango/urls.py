from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),


    #FIXME put regsiter link on top of base
    url(r'^register_dog_owner/$', views.register_dog_owner, name='register_dog_owner'),
    url(r'^register_hotel/$', views.register_hotel, name='register_hotel'),
    url(r'^register_sitter/$', views.register_sitter, name='register_sitter'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^delete/(?P<username_slug>[\w|\W.-]+)/$', views.user_deactivate, name='deactivate_user'),

    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    #those are the profile pages if u are a hotel owner dog owner or dogsitter  PERSONAL PAGES
    #url(r'^hot_detail/(?P<username_slug>[\w\-]+)/$', views.profile_load, name='get_hotel_profile'),
    #url(r'^sitter_detail/(?P<username_slug>[\w\-]+)/$', views.profile_load, name='get_dogsitter_profile'),
    #url(r'^dog_owner_detail/(?P<username_slug>[\w\-]+)/$', views.profile_load, name='get_dog_owner_profile'),
    url(r'^search/$', views.search, name='search'),


    url(r'^add_dog/$', views.add_dog, name='add_dog'),

]
