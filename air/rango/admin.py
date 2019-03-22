from django.contrib import admin
from rango.models import DogSitter, Hotel, DogOwner


'''
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes')
    prepopulated_fields = {'slug': ('name',)}


class DogSitterAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
'''
admin.site.register(DogSitter)
admin.site.register(Hotel)
admin.site.register(DogOwner)
