"""
persons/services/user_service_adapter.py (бизнес-логика)

This is service for a work only with a business logic for the Users (Persons)
"""

from typing import Optional

from django.core.mail import send_mail

from persons.exceptions import PersonErrorImproperlyConfigured
from persons.interfaces import EmailString, UsersPydantic
from persons.models import Users

# from allauth.account.internal.userkit import user_email


class PersonServiceAdapter:

    @staticmethod
    def get_user_by_id(user_id: Optional[int] = None) -> Optional[UsersPydantic]:
        """GEt user from the database and conversion through the Pydantic"""
        try:
            if user_id is not None and isinstance(user_id, int):
                user = Users.objects.get(id=user_id)
                return UsersPydantic.model_validate(user)
        except Users.DoesNotExist:
            return None
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))

    @staticmethod
    def get_user_by_email(
        user_email: Optional[EmailString] = None,
    ) -> Optional[UsersPydantic]:
        """GEt user from the database and conversion through the Pydantic"""
        try:
            if user_email is not None and isinstance(user_email, EmailString):
                user = Users.objects.get(email=user_email)
                return UsersPydantic.model_validate(user)
        except Users.DoesNotExist:
            return None
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        return None

    @staticmethod
    def search_by_email(email_pattern: str) -> list[UsersPydantic]:
        """Search users by email"""
        try:
            users = Users.objects.filter(email__icontains=email_pattern)
            return [UsersPydantic.model_validate(u) for u in users]
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))

    @staticmethod
    def send_email_to_user(user_id: int, subject: str, message: str):
        """Send email (in the database Person)"""
        try:
            user = Users.objects.get(id=user_id)
            send_mail(subject, message, None, [user.email])
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))

    @staticmethod
    def update_user_in_database(
        user_data: dict,
        user_id: Optional[int] = None,
        user_email: Optional[EmailString] = None,
    ) -> UsersPydantic:
        """
        Update user in database using Pydantic for validation

        Args:
            :param user_data: Dictionary with fields to update
            :param user_id: User ID (optional)
            :param user_email: User email (optional)

        Returns:
            Updated user as Pydantic model
        """
        get_person_model_old: Optional[UsersPydantic] = None

        try:
            get_person_model_old = PersonServiceAdapter.get_user_by_id(user_id)
        except PersonErrorImproperlyConfigured as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        if get_person_model_old is None:
            try:
                get_person_model_old = PersonServiceAdapter.get_user_by_email(
                    user_email
                )
            except PersonErrorImproperlyConfigured as e:
                raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
        if get_person_model_old is None:
            raise PersonErrorImproperlyConfigured("User not found.")

        try:

            person_model_old_to_dict: dict = get_person_model_old.model_dump()
            person_pydantic_new_user = UsersPydantic(**person_model_old_to_dict)
            # Below we create a model and update's field
            person_pydantic_user_data = UsersPydantic.model_validate(user_data)
            person_new_user_data = person_pydantic_user_data.model_dump()
            # exclude of fields
            forbidden_fields = {"id", "created_at", "date_joined"}
            update_dict: dict = {
                k: person_new_user_data.pop(k)
                for k, v in person_model_old_to_dict.items()
                if k not in forbidden_fields
            }
            if not update_dict:
                return get_person_model_old
            # ============================================
            # Here is UPDATING DATA IN DATABASE and return dictionary.
            # ============================================
            Users.objects.filter(email=person_pydantic_new_user.id).update(
                **update_dict
            )
            updated_user = Users.objects.get(id=person_pydantic_new_user.id)
            return UsersPydantic.model_validate(updated_user)
        except Exception as e:
            raise PersonErrorImproperlyConfigured(e.args[0] if e.args else str(e))
