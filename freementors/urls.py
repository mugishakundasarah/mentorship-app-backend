from django.contrib import admin
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from mentorship.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mentorship.urls')),
]
