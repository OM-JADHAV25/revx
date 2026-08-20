from enum import Enum


class FailureReason(str, Enum):
    INSUFFICIENT_FUNDS = "insufficient_funds"
    CARD_EXPIRED = "card_expired"
    PAYMENT_METHOD_DECLINED = "payment_method_declined"
    AUTHENTICATION_REQUIRED = "authentication_required"
    PROCESSING_ERROR = "processing_error"
    NETWORK_ERROR = "network_error"
    UNKNOWN = "unknown"