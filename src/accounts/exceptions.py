from exceptions import InvalidItemRequest, ItemNotFound


class AccountNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(AccountNotFound, self).__init__(
            msg=msg or "Account not found", error_trace=error_trace)


class UsernameAlreadyExists(InvalidItemRequest):
    def __init__(self, msg=None, error_trace=None):
        super(UsernameAlreadyExists, self).__init__(
            msg=msg or "Username already exists", error_trace=error_trace)
