from auth.service import AuthService
from accounts.persistence import AccountsPersistence
from accounts.service import AccountsService
from realms.persistence import RealmsPersistence
from realms.service import RealmsService


class ApplicationContext():
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ApplicationContext, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.accounts_persistence = AccountsPersistence()
        self.accounts = AccountsService(
            self.accounts_persistence)

        self.authentication = AuthService(
            self.accounts_persistence
        )

        self.realms_persistence = RealmsPersistence()
        self.realms = RealmsService(
            self.realms_persistence
        )
