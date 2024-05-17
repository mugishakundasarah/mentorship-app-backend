import graphene
import graphql_jwt
from graphql_jwt.shortcuts import create_refresh_token, get_token
from .models import User, MentorshipSession
from .types import UserType, MentorshipSessionType
from graphql_jwt.decorators import login_required


# All Mutations
class RequestSessionMutation(graphene.Mutation):
    class Arguments:
        mentorId = graphene.Int(required=True)

    session_request = graphene.Field(MentorshipSessionType)

    @staticmethod
    def mutate(root, info, mentorId):
        if info.context.user.role != 'mentee':
            raise Exception("You must be a mentee to request a session.")
        mentee = User.objects.get(id=info.context.user.id)
        mentor = User.objects.get(id=mentorId)
        session_request = MentorshipSession.objects.create(mentee=mentee, mentor=mentor)
        
        return RequestSessionMutation(session_request=session_request)

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

    def mutate(root, info, **kwargs):
        user = info.context.user
        if user.role == 'mentee':
            user.role = 'mentor'
            user.save()
            return RequestToBeMentor(user=user)
        else:
            # If the user is not a mentee, raise an exception
            raise Exception("You must be a mentee to request to be a mentor.")

class AcceptRequest(graphene.Mutation):
    class Arguments:
        request_id = graphene.ID()

    session = graphene.Field(MentorshipSessionType)

    def mutate(self, info, request_id):
        if info.context.user.role != 'mentor':
            raise Exception("You must be a mentor to accept a request.")
        session = MentorshipSession.objects.get(pk=request_id)
        session.status = 'accepted'
        session.save()
        
        return AcceptRequest(session=session)

class RejectRequest(graphene.Mutation):
    class Arguments:
        request_id = graphene.ID()

    session = graphene.Field(MentorshipSessionType)

    def mutate(self, info, request_id):
        if info.context.user.role != 'mentor':
            raise Exception("You must be a mentor to reject a request.")
        session = MentorshipSession.objects.get(pk=request_id)
        session.status = 'declined'
        session.save()
        
        return RejectRequest(session=session)
    
class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    register_user = RegisterUser.Field()
    request_to_be_mentor = RequestToBeMentor.Field()
    request_session = RequestSessionMutation.Field()
    accept_request = AcceptRequest.Field()
    reject_request = RejectRequest.Field()

# All Queries
class Query(graphene.ObjectType):
    all_mentors = graphene.List(UserType)
    mentor_by_id = graphene.Field(UserType, id=graphene.Int())
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    requests = graphene.List(MentorshipSessionType)
    
    @login_required
    def resolve_all_mentors(self, info, **kwargs):
        print("info")
        return User.objects.filter(role='mentor')

    def resolve_requests(self, info):
        # Get the logged-in user
        user = info.context.user
        
        # Check if the user is authenticated
        if not user.is_authenticated:
            raise Exception('User is not authenticated')

        # If the user is a mentor, return requests made to the mentor
        if user.role == 'mentor':
            return MentorshipSession.objects.filter(mentor=user)

        # If the user is a mentee, return requests made by the mentee
        elif user.role == 'mentee':
            return MentorshipSession.objects.filter(mentee=user)

        # If the user's role is neither mentor nor mentee, raise an exception
        else:
            raise Exception('Invalid user role')

    def resolve_mentor_by_id(self, info, id):
        try:
            return User.objects.get(id=id, role='mentor')
        except User.DoesNotExist:
            return None

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication Failure: You must be signed in")
        return user

    @graphql_jwt.decorators.login_required
    def resolve_users(self, info):
        return User.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutation)
