from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True    # этот кастомный менеджер будет использоваться в миграциях (процесс изменения базы данных в соответствии с изменениями моделей).

    def _create_user(self, email, password, **kwargs):  # Этот метод используется для создания обычного пользователя (не суперпользователя).
        if not email:
            return ValueError('Mail should definitely be handed over ')
        email = self.normalize_email(email=email)   # переводим его в нижний регистр
        user = self.model(email=email, **kwargs)
        phone_number = kwargs.get('phone number')
        if phone_number:
            user.create_phone_number_code()
        else:
            user.create_activation_code()
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('У суперюзера должно быть поле is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('У супер юзера должно быть поле is_superuser=True')
        return self._create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # AbstractUser уже содержит базовую функциональность для работы с пользователями, но мы дополнили ее новыми полями и функциональностью.
    password = models.CharField(max_length=100)
    activation_code = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    is_active = models.BooleanField(default=False, help_text='This field is used to activate the user')

    phone_number = models.CharField(max_length=25, blank=True, null=True, unique=True)

    objects = UserManager() # Это атрибут objects, который указывает, что для этой модели будет использоваться кастомный менеджер

    USERNAME_FIELD = 'email' # Это атрибут, который определяет, какое поле будет использоваться для аутентификации пользователя. В данном случае, для аутентификации пользователя будет использоваться поле email.
    REQUIRED_FIELDS = [] # Это список дополнительных полей, которые будут обязательными при создании пользователя через команду createsuperuser. В данном случае, нет дополнительных обязательных полей, так как все необходимые поля определены выше.

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid # генерирует уникальный идентификатор
        code = str(uuid.uuid4()) # uuid.uuid4(): Вызов функции uuid4() из модуля uuid создает новый UUID версии 4 (случайный UUID).
        self.activation_code = code # Мы преобразуем сгенерированный UUID в строку с помощью функции str(), так как поле activation_code в модели

    def create_phone_number_code(self):
        code = get_random_string(6, allowed_chars='123456789')
        self.activation_code = code
        return code