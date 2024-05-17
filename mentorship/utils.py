from graphql_jwt.decorators import login_required
from graphql_jwt.utils import jwt_payload
from functools import wraps
import jwt

def custom_jwt_payload_handler(user, context=None):
    payload = jwt_payload(user, context)
    # Add user's role to the payload
    payload['role'] = user.role

    return payload



def mentor_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        user = kwargs.get('info').context.user
        if user.role != 'mentor':
            raise Exception("You don't have permission to access this resource.")
        return func(*args, **kwargs)
    return wrapper

def mentee_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        info = kwargs.get('info')
        if info is None or not hasattr(info, 'context') or not hasattr(info.context, 'user'):
            print("yes info is none")
            raise Exception("Authentication Failure: User context not available.")
        print("reachedd")
        token = info.context.headers.get('authorization')
        token = token.split(' ')[1]
        print("token")
        print(token)
        
        user = info.context.user
        
        if user.role != 'mentee':
            raise Exception("Authorization Failure: You don't have permission to access this resource.")
        
        return func(*args, **kwargs)
    return wrapper


