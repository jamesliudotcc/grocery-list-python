from django.contrib import admin
from .models import Store, Item, House

# Register your models here.
admin.site.register(House)
admin.site.register(Item)
admin.site.register(Store)
