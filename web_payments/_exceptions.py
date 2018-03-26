# better include from web_payments

__all__ = []

class RedirectNeeded(Exception):
    pass

class ExternalPostNeeded(Exception):
    pass

class PaymentError(Exception):
    def __init__(self, message, code=None, gateway_message=None):
        super().__init__(message)
        self.code = code
        self.gateway_message = gateway_message

class NotInitialized(NotImplementedError):
    pass

class NotSupported(Exception):
    pass
