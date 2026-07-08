# persons/views/serializers/token_obtain_serializer.py:1
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as DRFJWTSerializer,
)


class TokenObtainPairSerializer(DRFJWTSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print("--------------")
        print(token)
        # Add custom claims
        token["username"] = user.username
        # ...

        return token

    def validate(self, attrs):
        # Стандартная валидация из родительского класса
        data = super().validate(attrs)

        # Добавляем user_id в токен при создании через validate
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
