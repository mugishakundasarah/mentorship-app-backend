# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

@csrf_exempt
def graphql_view(request):
    if request.method == 'POST':
        return GraphQLView.as_view(graphiql=True)(request)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
