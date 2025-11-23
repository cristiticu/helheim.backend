from exceptions import AuthorizationException, InvalidItemRequest, ItemNotFound


class InsufficientRealmPermissions(AuthorizationException):
    def __init__(self, msg=None, error_trace=None):
        super(InsufficientRealmPermissions, self).__init__(
            msg=msg or "Insufficient permissions for realm", error_trace=error_trace)


class RealmListFileNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(RealmListFileNotFound, self).__init__(
            msg=msg or "Realm list file not found", error_trace=error_trace)


class RealmNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(RealmNotFound, self).__init__(
            msg=msg or "Realm not found", error_trace=error_trace)


class RealmUserNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(RealmUserNotFound, self).__init__(
            msg=msg or "Realm user not found", error_trace=error_trace)


class PortalAlreadyOpened(InvalidItemRequest):
    def __init__(self, msg=None, error_trace=None):
        super(PortalAlreadyOpened, self).__init__(
            msg=msg or "A portal is already open to this world", error_trace=error_trace)


class PasswordTooShort(InvalidItemRequest):
    def __init__(self, msg=None, error_trace=None):
        super(PasswordTooShort, self).__init__(
            msg=msg or "The provided password is too short", error_trace=error_trace)


class WorldNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(WorldNotFound, self).__init__(
            msg=msg or "Realm world not found", error_trace=error_trace)


class InvalidRealmListFileName(InvalidItemRequest):
    def __init__(self, msg=None, error_trace=None):
        super(InvalidRealmListFileName, self).__init__(
            msg=msg or "Invalid realm list file name. Valid options are adminlist.txt, permittedlist.txt, bannedlist.txt", error_trace=error_trace)
