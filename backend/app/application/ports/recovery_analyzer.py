from __future__ import annotations

from typing import Protocol

from app.domain.entities.recovery_case import RecoveryCase
from app.domain.models.recovery_proposal import RecoveryProposal


class RecoveryAnalyzer(Protocol):
    """Analyzes a recovery case and produces a recovery proposal."""

    def analyze(
        self,
        *,
        recovery_case: RecoveryCase,
    ) -> RecoveryProposal:
        ...