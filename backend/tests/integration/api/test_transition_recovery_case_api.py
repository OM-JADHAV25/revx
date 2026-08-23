from fastapi.testclient import TestClient

from app.main import app


def create_recovery_case(client: TestClient) -> str:
    """Create a recovery case and return its identifier."""

    response = client.post(
        "/recovery-cases/analyze",
        json={
            "merchant_id": (
                "11111111-1111-1111-1111-111111111111"
            ),
            "payment_id": (
                "22222222-2222-2222-2222-222222222222"
            ),
            "amount": 1000,
            "currency": "INR",
            "retry_count": 0,
        },
    )

    assert response.status_code == 200

    return response.json()["recovery_case_id"]


def test_transitions_recovery_case_successfully() -> None:
    """A valid recovery case transition should succeed."""

    with TestClient(app) as client:
        recovery_case_id = create_recovery_case(client)

        get_response = client.get(
            f"/recovery-cases/{recovery_case_id}",
        )

        assert get_response.status_code == 200

        previous_version = get_response.json()["version"]

        response = client.patch(
            f"/recovery-cases/{recovery_case_id}/status",
            json={"target_status": "executing"},
        )

        assert response.status_code == 200

        body = response.json()

        assert body["recovery_case_id"] == recovery_case_id
        assert body["status"] == "executing"
        assert body["version"] == previous_version + 1


def test_returns_404_when_transitioning_missing_recovery_case() -> None:
    """Transitioning a missing recovery case should return 404."""

    with TestClient(app) as client:
        response = client.patch(
            "/recovery-cases/"
            "11111111-1111-1111-1111-111111111111/status",
            json={
                "target_status": "analyzing",
            },
        )

        assert response.status_code == 404

        assert response.json() == {"detail": "Recovery case not found."}


def test_returns_409_for_invalid_recovery_case_transition() -> None:
    """An invalid recovery case transition should return HTTP 409."""

    with TestClient(app) as client:
        recovery_case_id = create_recovery_case(client)

        response = client.patch(
            f"/recovery-cases/{recovery_case_id}/status",
            json={
                "target_status": "analyzing",
            },
        )

        assert response.status_code == 409

        body = response.json()

        assert body["detail"] == (
            "Invalid recovery state transition: "
            "action_approved -> analyzing."
        )