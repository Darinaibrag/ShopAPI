from django.db import models
from django.contrib.auth import get_user_model # Эта функция позволяет получить модель пользователя, которая определена в проекте, и может быть настроена через AUTH_USER_MODEL в файле настроек проекта. Это сделано для поддержки пользовательских моделей.
from category.models import Category
from ckeditor.fields import RichTextField
# Create your models here.

User = get_user_model() # Здесь мы получаем модель пользователя из функции get_user_model() и присваиваем ее переменной User. Таким образом, мы можем использовать эту модель для создания связи между моделями Product и User.




class Product(models.Model):
    STATUS_CHOICES = (('in_stock', 'В наличии'), ('out_of_stock', 'Нет в наличии')) # первый элемент - значение, которое будет сохранено в базе данных, а второй элемент - человекочитаемое представление этого значения.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='images')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.CharField(max_length=50, choices=STATUS_CHOICES) # Указывает человекочитаемое название модели в единственном числе.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'