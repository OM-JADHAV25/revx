from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.api.dependencies import (get_transition_recovery_case_use_case)
from app.domain.exceptions import (RecoveryCaseConcurrencyError)
from app.main import app


def test_returns_409_for_recovery_case_concurrency_conflict() -> None:
    """Concurrency conflicts should be translated to HTTP 409."""

    mock_use_case = Mock()

    mock_use_case.execute.side_effect = (
        RecoveryCaseConcurrencyError("Recovery case was modified concurrently.")
    )

    app.dependency_overrides[
        get_transition_recovery_case_use_case
    ] = lambda: mock_use_case

    try:
        with TestClient(app) as client:
            response = client.patch(
                "/recovery-cases/"
                "11111111-1111-1111-1111-111111111111"
                "/status",
                json={"target_status": "executing"},
            )

        assert response.status_code == 409

        assert response.json() == {
            "detail": (
                "Recovery case was modified concurrently. "
                "Please retry."
            ),
        }

    finally:
        app.dependency_overrides.clear()