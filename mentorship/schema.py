import graphene
import graphql_jwt
from graphql_jwt.shortcuts import create_refresh_token, get_token
from .models import User
from .types import UserType
from graphql_jwt.decorators import login_required
from .utils import mentee_required

class RegisterUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)
        role = graphene.String(required=True)
        bio = graphene.String()
        occupation = graphene.String()
        expertise = graphene.String()

    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    def mutate(self, info, email, password, firstName, lastName, role, bio='', occupation='', expertise=''):
        # Create the user
        user = User.objects.create(
            email=email,
            firstName=firstName,
            lastName=lastName,
            role=role,
            bio=bio,
            occupation=occupation,
            expertise=expertise
        )
        user.set_password(password)
        user.save()

        # Create tokens
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return RegisterUser(user=user, token=token, refresh_token=refresh_token)
    
class RequestToBeMentor(graphene.Mutation):
    class Arguments:
        pass 

    user = graphene.Field(UserType)

    @mentee_required
    def mutate(self, info):
        user = info.context.user
        if user.role == 'mentee':
            user.role = 'mentor'
            user.save()
            return RequestToBeMentor(user=user)
        else:
            # If the user is not a mentee, raise an exception
            raise Exception("You must be a mentee to request to be a mentor.")

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    register_user = RegisterUser.Field()
    request_to_be_mentor = RequestToBeMentor.Field()

class Query(graphene.ObjectType):
    all_mentors = graphene.List(UserType)
    mentor_by_id = graphene.Field(UserType, id=graphene.Int())
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    
    def resolve_all_mentors(self, info, **kwargs):
        return User.objects.filter(role='mentor')

    def resolve_mentor_by_id(self, info, id):
        try:
            return User.objects.get(id=id, role='mentor')
        except User.DoesNotExist:
            return None

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication Failure: You must be signed in")
        return user

    @graphql_jwt.decorators.login_required
    def resolve_users(self, info):
        return User.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutation)
