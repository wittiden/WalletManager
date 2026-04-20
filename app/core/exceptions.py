class EmailValueExistsError(Exception): pass
class UserIsBlockedError(Exception): pass
class UserIsNotBlockedError(Exception): pass
class PasswordValueNotExistsError(Exception): pass
class EmailValueNotExistsError(Exception): pass

class UserIsNotAdminError(Exception): pass
class UserIsNotClientError(Exception): pass
class AllParametersIsNoneError(Exception): pass

class NameFormatError(Exception): pass
class PasswordFormatError(Exception): pass
class AddressFormatError(Exception): pass

class PinFormatError(Exception): pass

class IsNoneError(Exception): pass
class IsEmptyError(Exception): pass
class IsInstanceError(Exception): pass

class WebElementNotFoundError(Exception): pass

class WalletIsBlockedError(Exception): pass
class WalletIsNotBlockedError(Exception): pass
