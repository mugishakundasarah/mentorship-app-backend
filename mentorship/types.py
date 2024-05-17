from graphene_django.types import DjangoObjectType
from .models import User, MentorshipSession

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'firstName', 'lastName', 'role', 'bio', 'occupation', 'expertise')

class MentorshipSessionType(DjangoObjectType):
    class Meta:
        model = MentorshipSession