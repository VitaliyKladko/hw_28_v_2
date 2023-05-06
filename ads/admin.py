from django.contrib import admin

from ads.models import Category, Ads, Location, Users

admin.site.register(Category)
admin.site.register(Ads)
admin.site.register(Location)
admin.site.register(Users)
