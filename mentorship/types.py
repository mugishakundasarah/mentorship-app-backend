import graphene
from graphene_django.types import DjangoObjectType
from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'firstName', 'lastName', 'role', 'bio', 'occupation', 'expertise')
