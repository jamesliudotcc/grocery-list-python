import datetime
import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType

from .models import Link, Store, Item, House


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class StoreType(DjangoObjectType):
    class Meta:
        model = Store


class ItemType(DjangoObjectType):
    class Meta:
        model = Item


class HouseType(DjangoObjectType):
    class Meta:
        model = House


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    store = graphene.Field(StoreType, id=graphene.Int())
    item = graphene.Field(ItemType, id=graphene.Int())
    house = graphene.Field(HouseType, id=graphene.Int())

    stores = graphene.List(StoreType, id=graphene.Int())
    items = graphene.List(ItemType, id=graphene.Int())
    houses = graphene.List(HouseType, id=graphene.Int())

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

    def resolve_stores(self, info, **kwargs):

        return Store.objects.all()

    def resolve_items(self, info, **kwargs):

        return Item.objects.all()

    def resolve_houses(self, info, **kwargs):

        return House.objects.all()

    def resolve_store(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Store.objects.get(pk=id)

    def resolve_item(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Item.objects.get(pk=id)

    def resolve_house(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return House.objects.get(pk=id)


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user or None

        link = Link(url=url, description=description, posted_by=user)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )


class CreateItem(graphene.Mutation):
    id = graphene.Int()
    house = graphene.Int()
    name = graphene.String()
    qty = graphene.Int()
    stores = graphene.List(graphene.Int)

    class Arguments:
        house = graphene.Int()
        name = graphene.String()
        qty = graphene.Int()
        stores = graphene.List(graphene.Int)

    def mutate(self, info, house, name, qty, stores):
        user = info.context.user or None
        # Only allow items to be added by house members
        house_for_item = House.objects.get(id=house)
        print(house_for_item)

        item = Item(name=name, qty=qty)
        item.save()
        item.houses.add(house_for_item)

        for store in stores:
            store_for_item = Store.objects.get(id=store)
            print(store_for_item)
            item.stores.add(store_for_item)

        # Fix by passing in object type correctly instead of this hack with integers
        return CreateItem(
            id=item.id,
            # house=item.houses.id,
            name=item.name,
            qty=item.qty,
            # stores=item.stores,
        )


class PurchaseItem(graphene.Mutation):
    ids = graphene.List(graphene.Int)

    class Arguments:
        ids = graphene.List(graphene.Int)

    def mutate(self, info, ids):
        user = info.context.user or None
        now = datetime.datetime.utcnow()

        for each_id in ids:
            item = Item.objects.get(id=each_id)
            item.bought = now
            item.bought_by = user
            item.save()

        return PurchaseItem(ids=ids)


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_item = CreateItem.Field()
    purchase_item = PurchaseItem.Field()
