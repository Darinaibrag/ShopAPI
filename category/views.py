from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from category.models import Category
from category.serializers import CategorySerializer
from rest_framework.permissions import AllowAny, IsAdminUser


# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']: # This checks if the action is 'retrieve' or 'list'. If so, it allows any user (AllowAny) to access these actions, meaning they don't need to be authenticated.
            return (AllowAny(),)
        return (IsAdminUser(),) # If the action is not 'retrieve' or 'list', it means the user is performing a more privileged action like creating, updating, or deleting a category. In such cases, only authenticated users with admin privileges (IsAdminUser) are allowed.