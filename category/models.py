from django.db import models
from django.utils.text import \
    slugify  # предоставляет функции для работы с текстом, включая функцию slugify, которая помогает создавать URL-подобные строки.


# Create your models here.

class Category(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True, blank=True)
    name = models.CharField(max_length=50, unique=True)

    def save(self, **kwargs): # не понимаю
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.save()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
