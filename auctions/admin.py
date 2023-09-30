from django.contrib import admin
from .models import Categories, Listings, Comments, Bids, User
# Register your models here.
admin.site.register(Categories)
admin.site.register(Listings)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(User)