from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import create_application


def create_client() -> TestClient:
    application = create_application()

    return TestClient(application)


def test_analyze_recovery_case_returns_approved_action() -> None:
    client = create_client()

    response = client.post(
        "/recovery-cases/analyze",
        json={
            "merchant_id": "11111111-1111-1111-1111-111111111111",
            "payment_id": "22222222-2222-2222-2222-222222222222",
            "amount": 1000,
            "currency": "INR",
            "retry_count": 0,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "action_approved"
    assert body["proposed_action"] == "retry_payment"
    assert body["policy_decision"] == "approved"
    assert body["recovery_probability"] == "0.85"
    assert body["risk_score"] == "0.15"


def test_analyze_recovery_case_approves_high_value_payment() -> None:
    client = create_client()

    response = client.post(
        "/recovery-cases/analyze",
        json={
            "merchant_id": "11111111-1111-1111-1111-111111111111",
            "payment_id": "22222222-2222-2222-2222-222222222222",
            "amount": 10000,
            "currency": "INR",
            "retry_count": 0,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "action_approved"
    assert body["proposed_action"] == "retry_payment"
    assert body["policy_decision"] == "approved"
    assert body["recovery_probability"] == "0.65"
    assert body["risk_score"] == "0.45"


def test_analyze_recovery_case_rejects_retry_limit() -> None:
    client = create_client()

    response = client.post(
        "/recovery-cases/analyze",
        json={
            "merchant_id": "11111111-1111-1111-1111-111111111111",
            "payment_id": "22222222-2222-2222-2222-222222222222",
            "amount": 1000,
            "currency": "INR",
            "retry_count": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "stopped"
    assert body["proposed_action"] == "retry_payment"
    assert body["policy_decision"] == "rejected"


def test_analyze_recovery_case_rejects_invalid_amount() -> None:
    client = create_client()

    response = client.post(
        "/recovery-cases/analyze",
        json={
            "merchant_id": "11111111-1111-1111-1111-111111111111",
            "payment_id": "22222222-2222-2222-2222-222222222222",
            "amount": 0,
            "currency": "INR",
            "retry_count": 0,
        },
    )

    assert response.status_code == 422


def test_analyze_recovery_case_rejects_negative_retry_count() -> None:
    client = create_client()

    response = client.post(
        "/recovery-cases/analyze",
        json={
            "merchant_id": "11111111-1111-1111-1111-111111111111",
            "payment_id": "22222222-2222-2222-2222-222222222222",
            "amount": 1000,
            "currency": "INR",
            "retry_count": -1,
        },
    )

    assert response.status_code == 422


def test_get_recovery_case_returns_existing_case() -> None:
    client = create_client()

    create_response = client.post(
        "/recovery-cases/analyze",
        json={
            "merchant_id": "11111111-1111-1111-1111-111111111111",
            "payment_id": "22222222-2222-2222-2222-222222222222",
            "amount": 1000,
            "currency": "INR",
            "retry_count": 0,
        },
    )

    assert create_response.status_code == 200

    recovery_case_id = create_response.json()["recovery_case_id"]

    response = client.get(
        f"/recovery-cases/{recovery_case_id}",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["recovery_case_id"] == recovery_case_id
    assert body["merchant_id"] == ("11111111-1111-1111-1111-111111111111")
    assert body["payment_id"] == ("22222222-2222-2222-2222-222222222222")
    assert body["amount"] == "1000"
    assert body["currency"] == "INR"


def test_get_recovery_case_returns_not_found_when_case_does_not_exist() -> None:
    client = create_client()

    response = client.get(
        f"/recovery-cases/{uuid4()}",
    )

    assert response.status_code == 404

    body = response.json()

    assert body["detail"] == "Recovery case not found."