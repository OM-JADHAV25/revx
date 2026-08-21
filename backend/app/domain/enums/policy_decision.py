from enum import Enum


class PolicyDecision(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"