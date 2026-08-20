from enum import Enum


class RecoveryAction(str, Enum):
    RETRY_PAYMENT = "retry_payment"
    REQUEST_PAYMENT_METHOD_UPDATE = "request_payment_method_update"
    REQUEST_AUTHENTICATION = "request_authentication"
    ESCALATE_TO_MERCHANT = "escalate_to_merchant"
    STOP_RECOVERY = "stop_recovery"