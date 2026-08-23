from __future__ import annotations

from pydantic import BaseModel

from app.domain.enums.recovery_status import RecoveryStatus


class TransitionRecoveryCaseRequest(BaseModel):
    """Request for transitioning a recovery case."""

    target_status: RecoveryStatus