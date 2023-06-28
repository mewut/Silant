from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return False
    

# На сайте запретите пользователям регистрацию. 
# Для этого в пакете allauth переопределите метод is_open_for_signup, он должен возвращать False.
# Подробнее в документации на django-allauth.readthedocs.io.  https://django-allauth.readthedocs.io/en/latest/advanced.html#creating-and-populating-user-instances
# Администратор может создавать пользователя в админ панели.