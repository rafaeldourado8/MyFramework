class DomainException(Exception):
    """Base domain exception"""
    pass


class ValidationException(DomainException):
    """Validation error"""
    pass


class BusinessRuleViolationException(DomainException):
    """Business rule violation"""
    pass


class NotFoundException(DomainException):
    """Entity not found"""
    pass
