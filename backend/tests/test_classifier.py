import pytest

from app.classifier.classifier import Classifier
from app.classifier.escalation import get_escalation, get_evidence
from app.classifier.risk import get_risk_level

clf = Classifier()


@pytest.mark.parametrize(
    "question,expected",
    [
        ("my credit card was charged 1000 without consent", "unauthorized_transaction"),
        ("unauthorized transaction otp fraud on my account", "unauthorized_transaction"),
        ("what is the 30 day rule for credit card complaints", "credit_card_grievance"),
        ("my credit card annual fee was charged, card complaint", "credit_card_grievance"),
        ("my upi payment failed but money was deducted", "upi_failed_transaction"),
        ("phonepe upi money deducted not credited", "upi_failed_transaction"),
        ("how do i contact the nodal officer", "support_contact_nodal_officer"),
        ("how to file complaint with rbi ombudsman", "ombudsman_escalation"),
        ("my account is frozen due to kyc", "kyc_or_identity"),
        ("cheque collection is delayed", "cheque_collection_delay"),
        ("claim process after death of account holder legal heir", "deceased_depositor_claim"),
        ("i cannot access my locker", "safe_deposit_locker"),
        ("my home loan emi increased after interest rate reset", "loan_complaint"),
        ("health insurance cashless hospitalization not approved", "insurance_health_claim"),
        ("car insurance own damage claim", "insurance_motor_claim"),
        ("minimum balance penalty charged on savings account", "deposit_account_service_charge"),
        ("should i buy mutual funds", "unsupported_or_advice_request"),
        ("should i invest in crypto currency", "unsupported_or_advice_request"),
        ("what is the best investment for tax saving", "unsupported_or_advice_request"),
    ],
)
def test_classify(question, expected):
    assert clf.classify(question)[0] == expected


def test_risk_levels():
    assert get_risk_level("unauthorized_transaction", "x") == "high"
    assert get_risk_level("deceased_depositor_claim", "x") == "high"
    assert get_risk_level("credit_card_grievance", "x") == "medium"
    assert get_risk_level("ombudsman_escalation", "x") == "low"
    assert get_risk_level("failed_transaction_tat", "x") == "low"
    assert get_risk_level("unsupported_or_advice_request", "x") == "not_applicable"


def test_upi_risk_escalates_with_wording():
    assert get_risk_level("upi_failed_transaction", "payment failed") == "medium"
    assert get_risk_level("upi_failed_transaction", "money stuck for a month unresolved") == "high"


def test_escalation_routes():
    upi = get_escalation("upi_failed_transaction")
    assert len(upi) == 3
    assert "cms.rbi.org.in" in upi[-1]
    assert any("Ombudsman" in s for s in get_escalation("insurance_grievance"))
    assert get_escalation("unsupported_or_advice_request") == []


def test_evidence_checklists():
    assert len(get_evidence("unauthorized_transaction")) >= 3
    assert get_evidence("unsupported_or_advice_request") == []
