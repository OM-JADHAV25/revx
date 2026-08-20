from enum import Enum


class RecoveryStatus(str, Enum):
    DETECTED = "detected"
    ANALYZING = "analyzing"
    ELIGIBLE = "eligible"
    ACTION_PENDING = "action_pending"
    ACTION_APPROVED = "action_approved"
    EXECUTING = "executing"
    RETRY_SCHEDULED = "retry_scheduled"
    RECOVERED = "recovered"
    ESCALATED = "escalated"
    STOPPED = "stopped"