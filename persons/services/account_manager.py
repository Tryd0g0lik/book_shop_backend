# persons/services/account_manager.py:1


class AccountManager:
    def __new__(cls, *args, **kwargs):
        from persons.adapters import PostmanAdapter

        cls.postman = PostmanAdapter()
        return super().__new__(cls, *args, **kwargs)

    @staticmethod
    def inisialize_account():
        from persons.adapters.account_adapter import AccountAdapter

        return AccountAdapter()
