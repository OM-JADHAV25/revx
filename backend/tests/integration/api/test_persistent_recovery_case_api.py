from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_recovery_case_persists_across_api_clients() -> None:
    """Verify a recovery case persists beyond the original API client."""

    with TestClient(app) as create_client:
        create_response = create_client.post(
            "/recovery-cases/analyze",
            json={
                "merchant_id": ("11111111-1111-1111-1111-111111111111"),
                "payment_id": ("22222222-2222-2222-2222-222222222222"),
                "amount": 2500,
                "currency": "INR",
                "retry_count": 0,
            },
        )

        assert create_response.status_code == 200

        recovery_case_id = create_response.json()["recovery_case_id"]

    # New API client → new request lifecycle → new DB session.
    with TestClient(app) as get_client:
        get_response = get_client.get(
            f"/recovery-cases/{recovery_case_id}",
        )

        assert get_response.status_code == 200

        body = get_response.json()

        assert body["recovery_case_id"] == recovery_case_id

        assert body["merchant_id"] == ("11111111-1111-1111-1111-111111111111")

        assert body["payment_id"] == ("22222222-2222-2222-2222-222222222222")

        assert body["amount"] == "2500"

        assert body["currency"] == "INR"

        assert body["retry_count"] == 0