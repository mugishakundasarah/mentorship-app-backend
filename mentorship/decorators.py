from functools import wraps
from graphql import GraphQLError

def check_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to perform this action.")
        return func(*args, **kwargs)
    return wrapper
