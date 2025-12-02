class ZendFiError(Exception):
    """Base error for the SDK"""


class APIError(ZendFiError):
    def __init__(self, status_code: int, message: str, details=None):
        super().__init__(f"{status_code}: {message}")
        self.status_code = status_code
        self.details = details


class WebhookVerificationError(ZendFiError):
    pass
