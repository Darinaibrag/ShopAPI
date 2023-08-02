from django.core.mail import send_mail
from django.utils.html import format_html


# def send_confirmation_email(email, code):
#     send_mail(
#         'Hello, activate your account',
#         f'To activate your account copy and enter code on the website: {code}'
#         f'\n{code}'
#         f'\ndo not share with anyone',
#         'darinaibrag@gmail.com',
#         [email],
#         fail_silently=False
#     )

def send_confirmation_email(email, code):
    activation_url = f'http://127.0.0.1:8000/api/account/activate/?u={code}'
    message = format_html(
        'Здравствуйте, активируйте ваш аккаунт! '
        'Чтобы активировать ваш аккаунт, перейдите по ссылке:'
        '<br>'
        '<a href="{}">{}</a>'
        '<br>'
        'Не передавайте этот код никому!',
        activation_url, activation_url
    )

    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        message,
        'darinaibrag@gmail.com',
        [email],
        fail_silently=False,
    )