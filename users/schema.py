import datetime
from django.contrib.auth import get_user_model
from django.db import models
from lists.models import Invite

import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")

        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        token = graphene.String(required=False)

    def mutate(self, info, username, email, password, first_name, last_name, token):
        # Used to validate, not working, moving on for now.

        # def house_from_token(token, email):
        #     recent_invites = Invite.objects.filter(
        #         created__gte=(datetime.date.today() - datetime.timedelta(days=1))
        #     ).filter(email=email)
        #     print(recent_invites)

        #     valid_token = [t for t in recent_invites.all() if t.token == token][0]
        #     if valid_token:
        #         return 1

        #     return None

        user = get_user_model()(username=username, email=email)
        user.set_password(password)

        # if house_from_token(token, email):
        #     pass
        # else:
        #     print("ok, whatever")

        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

