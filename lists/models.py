from django.db import models
from django.conf import settings

# Create your models here.
class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )


class Store(models.Model):
    def __str__(self):
        return "Store: " + self.name

    name = models.CharField(max_length=50)


class Item(models.Model):
    def __str__(self):
        return "Item: " + self.name

    name = models.CharField(max_length=50)
    qty = models.IntegerField()
    stores = models.ManyToManyField(Store, blank=True, related_name="items")
    bought = models.DateField(default=None, blank=True, null=True)
    bought_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )


class House(models.Model):
    def __str__(self):
        return "House: " + self.name

    name = models.CharField(max_length=50)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="houses"
    )
    items = models.ManyToManyField(Item, blank=True, related_name="houses")
    faveStores = models.ManyToManyField(Store, blank=True, related_name="houses")


class Invite(models.Model):
    def __str__(self):
        return f"Token for {self.first_name}"

    token = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
