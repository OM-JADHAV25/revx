from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (InvalidRecoveryStateTransitionError,RecoveryCaseConcurrencyError)


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
            content={"detail": str(exc)},
        )

    @app.exception_handler(
        RecoveryCaseConcurrencyError,
    )
    async def handle_recovery_case_concurrency_error(
        request: Request,
        exc: RecoveryCaseConcurrencyError,
    ) -> JSONResponse:
        """Convert optimistic concurrency conflicts into HTTP 409."""

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": (
                    "Recovery case was modified concurrently. "
                    "Please retry."
                ),
            },
        )