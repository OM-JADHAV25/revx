from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import create_application


def test_analyze_recovery_case_is_idempotent_for_same_payment() -> None:
    """The same payment should always return the same recovery case."""

    application = create_application()

    merchant_id = str(uuid4())
    payment_id = str(uuid4())

    payload = {
        "merchant_id": merchant_id,
        "payment_id": payment_id,
        "amount": 1000,
        "currency": "INR",
        "retry_count": 0,
    }

    with TestClient(application) as client:
        first_response = client.post(
            "/recovery-cases/analyze",
            json=payload,
        )

        assert first_response.status_code == 200

        second_response = client.post(
            "/recovery-cases/analyze",
            json=payload,
        )

        assert second_response.status_code == 200

    first_body = first_response.json()
    second_body = second_response.json()

    assert (second_body["recovery_case_id"] == first_body["recovery_case_id"])

    assert (second_body["status"] == first_body["status"])

    assert (second_body["proposed_action"] == first_body["proposed_action"])

    assert (second_body["policy_decision"] == first_body["policy_decision"])

    assert (second_body["recovery_probability"] == first_body["recovery_probability"])

    assert (second_body["risk_score"] == first_body["risk_score"])