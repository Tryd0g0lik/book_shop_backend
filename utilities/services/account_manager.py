# persons/services/account_manager.py:1


class AccountManager:
    def __new__(cls, *args, **kwargs):
        from utilities.adapters import PostmanAdapter

        # from persons.interfaces.interface_postman import PostmanAdapter as AccountAdapterInitialize

        cls.postman = PostmanAdapter()
        return super().__new__(cls, *args, **kwargs)

    @staticmethod
    def inisialize_account():
        from utilities.adapters.account_adapter import AccountAdapter

        return AccountAdapter()
