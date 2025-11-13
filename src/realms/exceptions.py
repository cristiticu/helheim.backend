from exceptions import InvalidItemRequest, ItemNotFound


class RealmNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(RealmNotFound, self).__init__(
            msg=msg or "Realm not found", error_trace=error_trace)


class PortalAlreadyOpened(InvalidItemRequest):
    def __init__(self, msg=None, error_trace=None):
        super(PortalAlreadyOpened, self).__init__(
            msg=msg or "A portal is already open to this world", error_trace=error_trace)


class PasswordTooShort(InvalidItemRequest):
    def __init__(self, msg=None, error_trace=None):
        super(PasswordTooShort, self).__init__(
            msg=msg or "The provided password is too short", error_trace=error_trace)
