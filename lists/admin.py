from django.contrib import admin
from .models import Store, Item, House, Token

# Register your models here.
admin.site.register(House)
admin.site.register(Item)
admin.site.register(Store)
admin.site.register(Token)
