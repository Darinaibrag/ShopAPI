from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from product.models import Product
from product.serializers import ProductSerializer
from rest_framework import permissions
from product.permissions import IsAuthor
from rest_framework.decorators import action
from rating.serializers import RatingSerializers
from rest_framework.response import Response

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all() # Мы устанавливаем атрибут queryset, который определяет множество объектов, доступных для запросов к представлению. В данном случае, это все объекты Product.
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']: # Здесь мы проверяем текущее действие (self.action), и если это одно из: 'update', 'partial_update', 'destroy', то мы возвращаем кортеж из двух правил разрешений. Первое правило permissions.IsAuthenticated() требует, чтобы пользователь был аутентифицирован, чтобы выполнять эти действия, а второе правило IsAuthor() проверяет, является ли пользователь владельцем объекта, чтобы разрешить или запретить доступ к действиям.
            return permissions.IsAuthenticated(), IsAuthor()
        return (permissions.IsAuthenticatedOrReadOnly(),)

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def ratings(self, request, pk):
        product = self.get_object()
        user = request.user

        if request.method == 'POST':
            rating = product.ratings.all()
            serializer = RatingSerializers(instance = rating, many=True)
            return Response(serializer, status=200)

        elif request.method == 'POST':
            if product.ratings.filter(owner=user).exists():
                return Response('Вы уже поставили рейтинг')
            serializer = RatingSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return Response(serializer.data, status=201)
        else:
            if not product.ratings.filter(owner=user).exists():
                return Response('Вы не можете удалить, потому что вы не ставили рейтинг', status=400)
            rating = product.ratings.get(owner=user)
            rating.delete()
            return Response('Удалено', status=204)






