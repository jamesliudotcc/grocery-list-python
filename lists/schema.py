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
    stores = graphene.List(StoreType)
    items = graphene.List(ItemType)
    houses = graphene.List(HouseType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

    def resolve_stores(self, info, **kwargs):
        return Store.objects.all()

    def resolve_items(self, info, **kwargs):
        return Item.objects.all()

    def resolve_houses(self, info, **kwargs):
        return House.objects.all()


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


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
