from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (InvalidRecoveryStateTransitionError)


def register_exception_handlers(app: FastAPI) -> None:
    """Register application-wide exception handlers."""

    @app.exception_handler(
        InvalidRecoveryStateTransitionError,
    )
    async def handle_invalid_recovery_state_transition(
        request: Request,
        exc: InvalidRecoveryStateTransitionError,
    ) -> JSONResponse:
        """Convert invalid recovery state transitions into HTTP 409."""

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)}
        )