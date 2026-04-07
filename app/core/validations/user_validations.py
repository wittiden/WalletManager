from app.core.validations.exceptions import EmailFormatError, PasswordFormatError, NameFormatError
from app.core.validations.general_validations import GeneralValidation


class UserBaseValidation:
    """Класс для валидации объектов UserBase"""

    @staticmethod
    def valid_name(name: str) -> str:
        GeneralValidation.isinstance_checker(name, str)

        GeneralValidation.not_empty_checker(name)

        if any(letter.isdigit() or letter.isspace() for letter in name):
            raise NameFormatError(f'{name} has digits or spaces')

        return name

    @staticmethod
    def valid_email(email: str) -> str:
        GeneralValidation.isinstance_checker(email, str)

        GeneralValidation.not_empty_checker(email)

        if email.isspace():
            raise EmailFormatError(f'{email} has spaces')

        if email.count('@') != 1:
            raise EmailFormatError(f'{email} count("@") != 1')

        local, domain = email.split('@')

        GeneralValidation.not_empty_checker(local)
        GeneralValidation.not_empty_checker(domain)

        if domain.count('.') == 0:
            raise EmailFormatError(f'{domain} count(".") == 0')

        if domain[0] == '.' or domain[-1] == '0':
            raise EmailFormatError(f'{domain} first or second letter == "."')

        return email

    @staticmethod
    def valid_is_blocked(is_blocked: bool) -> bool:
        GeneralValidation.isinstance_checker(is_blocked, bool)

        return is_blocked

    @staticmethod
    def valid_password(password: str) -> str:
        GeneralValidation.isinstance_checker(password, str)

        GeneralValidation.not_empty_checker(password)

        if len(password) < 8:
            raise PasswordFormatError(f'{password} length < 8')

        return password