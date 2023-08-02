from rest_framework import serializers
from product.models import Product
from django.db.models import Avg


class ProductSerializer(serializers.ModelSerializer): # Таким образом, этот сериализатор ProductSerializer позволяет преобразовать объекты модели Product в формат JSON, включая информацию об идентификаторе владельца и его электронной почте. При десериализации, когда вы получаете данные из API, эти два поля будут доступны только для чтения и не будут использоваться при обновлении объектов Product
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))
        rating = representation['rating']
        rating['rating_count'] = instance.ratings.count()
        return representation