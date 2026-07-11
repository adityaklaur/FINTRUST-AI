"""Issue taxonomy: categories, risk levels, escalation routes, evidence lists.

This is deliberately deterministic and code-owned (not LLM-generated) because
escalation routes and risk levels are safety-critical: a wrong ombudsman route
or a downplayed fraud risk is worse than a clumsy sentence. The LLM writes the
*prose*; this file owns the *structured guidance*.

Escalation routes are grounded in Indian frameworks: RB-IOS 2026 (RBI CMS,
cms.rbi.org.in) for banking; Bima Bharosa / IRDAI + Insurance Ombudsman
(Insurance Ombudsman Rules 2017) for insurance.
"""

from __future__ import annotations

# category -> keyword list (matched as lowercase substrings of the question)
CATEGORIES: dict[str, list[str]] = {
    "credit_card_grievance": [
        "credit card", "card complaint", "card charge", "annual fee",
        "card block", "card statement", "late fee", "card decline",
    ],
    "upi_failed_transaction": [
        "upi", "payment failed", "money deducted", "not credited",
        "upi help", "gpay", "phonepe", "paytm", "bhim",
    ],
    "unauthorized_transaction": [
        "unauthorized", "unauthorised", "fraudulent", "hacked", "unknown debit",
        "otp fraud", "phishing", "without consent", "without my knowledge",
        "did not do", "didn't do", "not done by me", "stolen card",
    ],
    "failed_transaction_tat": [
        "tat", "turn around", "100 per day", "compensation for failed",
        "t+1", "t+5", "auto reversal", "reversal timeline",
    ],
    "kyc_or_identity": [
        "kyc", "know your customer", "aml", "re-kyc", "account frozen",
        "account freeze", "identity proof", "update kyc", "periodic kyc",
    ],
    "ombudsman_escalation": [
        "ombudsman", "rbi complaint", "cms portal", "integrated ombudsman",
        "escalate to rbi", "rb-ios", "cms.rbi",
    ],
    "support_contact_nodal_officer": [
        "nodal officer", "principal nodal", "pno", "grievance officer",
        "customer care number", "contact the bank", "helpline",
    ],
    "cheque_collection_delay": [
        "cheque", "outstation cheque", "cheque collection", "instrument",
        "cheque cleared", "cheque bounce",
    ],
    "deposit_account_service_charge": [
        "minimum balance", "account closure", "service charge", "penalty charge",
        "inoperative account", "non maintenance", "amb",
    ],
    "deceased_depositor_claim": [
        "deceased", "death claim", "nominee claim", "legal heir",
        "after death", "died", "passed away", "succession",
    ],
    "safe_deposit_locker": [
        "locker", "safe deposit", "locker access", "locker rent", "locker contents",
    ],
    "loan_complaint": [
        "loan", "emi", "interest rate", "foreclosure", "penal charge",
        "kfs", "prepayment", "tenor", "moratorium",
    ],
    "insurance_health_claim": [
        "health insurance", "cashless", "reimbursement claim", "hospitalization",
        "tpa", "mediclaim", "pre-authorization",
    ],
    "insurance_motor_claim": [
        "motor insurance", "car insurance", "own damage", "third party claim",
        "vehicle theft", "accident claim", "idv",
    ],
    "insurance_grievance": [
        "insurance ombudsman", "irdai", "bima bharosa", "insurer",
        "claim rejected", "policy lapse", "insurance complaint",
    ],
    "unsupported_or_advice_request": [
        "should i invest", "which fund", "mutual fund", "crypto",
        "stock market", "tax saving", "legal opinion", "guaranteed return",
        "best investment", "portfolio advice",
    ],
}

# Ordered most-specific / most-severe first; ties in keyword count break toward
# the earlier entry so "credit card charged without consent" -> unauthorized.
CATEGORY_PRIORITY: list[str] = [
    "unauthorized_transaction",
    "deceased_depositor_claim",
    "upi_failed_transaction",
    "failed_transaction_tat",
    "ombudsman_escalation",
    "kyc_or_identity",
    "loan_complaint",
    "cheque_collection_delay",
    "safe_deposit_locker",
    "deposit_account_service_charge",
    "insurance_health_claim",
    "insurance_motor_claim",
    "insurance_grievance",
    "credit_card_grievance",
    "support_contact_nodal_officer",
]

# Phrases that indicate the user is asking for advice we must NOT give.
# Chosen to avoid false hits (e.g. "investment" not bare "invest" -> "investigation").
STRONG_ADVICE: list[str] = [
    "invest in", "investment", "crypto", "bitcoin", "mutual fund",
    "stock market", "share market", "tax saving", "legal opinion",
    "guaranteed return", "best investment", "portfolio", "buy shares",
    "which stock", "advise me",
]

RISK_RULES: dict[str, list[str]] = {
    "high": ["unauthorized_transaction", "deceased_depositor_claim"],
    "medium": [
        "credit_card_grievance", "cheque_collection_delay", "kyc_or_identity",
        "loan_complaint", "insurance_health_claim", "insurance_motor_claim",
        "insurance_grievance",
    ],
    "low": [
        "deposit_account_service_charge", "safe_deposit_locker",
        "support_contact_nodal_officer", "ombudsman_escalation",
        "failed_transaction_tat",
    ],
    "not_applicable": ["unsupported_or_advice_request"],
}

# Words that escalate a UPI failed-transaction from medium to high.
UPI_ESCALATION_WORDS: list[str] = [
    "stuck", "month", "weeks", "unresolved", "30 day", "not resolved", "still not",
]

_RBI_CMS = "https://cms.rbi.org.in"

ESCALATION_ROUTES: dict[str, list[str]] = {
    "credit_card_grievance": [
        "Step 1: Contact the card issuer's customer care and note your complaint reference number.",
        "Step 2: If unresolved within 30 days, escalate to the bank's Grievance Redressal / Nodal Officer.",
        f"Step 3: If still unresolved, file a complaint at {_RBI_CMS} under RB-IOS 2026.",
    ],
    "upi_failed_transaction": [
        "Step 1: Raise a dispute in your UPI app (open the transaction → UPI Help / Raise Dispute).",
        "Step 2: If unresolved, contact your bank/PSP customer care with the UTR / transaction ID.",
        f"Step 3: If the bank does not resolve it within 30 days, file at {_RBI_CMS}.",
    ],
    "unauthorized_transaction": [
        "Step 1: Immediately notify your bank via its 24x7 fraud / unauthorized-transaction helpline.",
        "Step 2: Block the affected card or account and record the acknowledgement.",
        "Step 3: File a written complaint. The source describes a shadow-reversal / limited-liability framework when reported promptly.",
        f"Step 4: If unresolved, escalate to the bank's Nodal Officer and then {_RBI_CMS}.",
    ],
    "failed_transaction_tat": [
        "Step 1: Raise the failed transaction with your bank / PSP quoting the transaction reference.",
        "Step 2: Ask about auto-reversal and any TAT-based compensation the source describes.",
        f"Step 3: If not resolved/compensated per the framework, file at {_RBI_CMS}.",
    ],
    "kyc_or_identity": [
        "Step 1: Submit the requested KYC documents to your branch or through the bank's app.",
        "Step 2: If the account is restricted and the issue persists, escalate to the Grievance Redressal Officer.",
        f"Step 3: For deficiency in service, you may complain at {_RBI_CMS}.",
    ],
    "ombudsman_escalation": [
        "Step 1: Ensure you first complained to the bank AND 30 days passed (or it was rejected).",
        f"Step 2: File your complaint online at {_RBI_CMS} under the RB-IOS 2026 scheme.",
        "Step 3: Track the complaint and respond to the Ombudsman's requests via the CMS portal.",
    ],
    "support_contact_nodal_officer": [
        "Step 1: Contact the institution's customer care with your details and reference number.",
        "Step 2: If unresolved, escalate to the Principal Nodal Officer / Grievance Redressal Officer.",
        f"Step 3: If still unresolved, escalate to the RBI Ombudsman at {_RBI_CMS}.",
    ],
    "cheque_collection_delay": [
        "Step 1: Raise the delay with your branch, quoting the instrument details.",
        "Step 2: Escalate to the Grievance Redressal Officer citing the bank's Cheque Collection Policy.",
        f"Step 3: If unresolved, complain at {_RBI_CMS}.",
    ],
    "deposit_account_service_charge": [
        "Step 1: Ask the branch for the applicable charge schedule and the basis of the charge.",
        "Step 2: Escalate to the Grievance Redressal Officer if it appears incorrect.",
        f"Step 3: If unresolved, complain at {_RBI_CMS}.",
    ],
    "deceased_depositor_claim": [
        "Step 1: Submit the death certificate and nomination / legal-heir documents to the branch.",
        "Step 2: If settlement is delayed beyond the stated timeline, escalate to the Grievance Redressal Officer.",
        f"Step 3: If unresolved, complain at {_RBI_CMS}. (If the bank itself has failed, deposit insurance via DICGC may apply.)",
    ],
    "safe_deposit_locker": [
        "Step 1: Raise the issue with your branch, citing your locker agreement.",
        "Step 2: Escalate to the Grievance Redressal Officer citing RBI's locker guidelines.",
        f"Step 3: If unresolved, complain at {_RBI_CMS}.",
    ],
    "loan_complaint": [
        "Step 1: Contact the lender's customer care with your loan account number and the Key Fact Statement (KFS).",
        "Step 2: Escalate to the Grievance Redressal / Nodal Officer if unresolved.",
        f"Step 3: If still unresolved, complain at {_RBI_CMS}.",
    ],
    "insurance_health_claim": [
        "Step 1: Raise the claim issue with your insurer / TPA and note the claim number.",
        "Step 2: Escalate to the insurer's Grievance Redressal Officer (GRO).",
        "Step 3: If unresolved, use IRDAI's Bima Bharosa portal, then the Insurance Ombudsman.",
    ],
    "insurance_motor_claim": [
        "Step 1: Raise the claim with your insurer / surveyor and note the claim number.",
        "Step 2: Escalate to the insurer's Grievance Redressal Officer (GRO).",
        "Step 3: If unresolved, use IRDAI's Bima Bharosa portal, then the Insurance Ombudsman.",
    ],
    "insurance_grievance": [
        "Step 1: File your grievance with the insurer's Grievance Redressal Officer (GRO).",
        "Step 2: If unresolved in the stated time, escalate via IRDAI's Bima Bharosa portal.",
        "Step 3: Approach the Insurance Ombudsman under the Insurance Ombudsman Rules, 2017.",
    ],
    "unsupported_or_advice_request": [],
}

EVIDENCE_CHECKLISTS: dict[str, list[str]] = {
    "credit_card_grievance": [
        "Card number (last 4 digits) and statement showing the disputed item",
        "Date and amount of the disputed charge",
        "Complaint reference number and date first raised",
        "Any emails/SMS from the issuer",
    ],
    "upi_failed_transaction": [
        "UTR / transaction ID and UPI app used",
        "Date, time and amount of the transaction",
        "Screenshot of the failed/pending status",
        "Bank account debit SMS/statement entry",
    ],
    "unauthorized_transaction": [
        "Exact date, time and amount of each unauthorized transaction",
        "SMS/email alerts you received",
        "Date & time you reported it to the bank + acknowledgement number",
        "Whether OTP/card/credentials were shared or lost (and any FIR, if filed)",
    ],
    "failed_transaction_tat": [
        "Transaction reference and the payment system used",
        "Date of transaction and current status",
        "Any reversal/compensation communication from the bank",
    ],
    "kyc_or_identity": [
        "Officially valid documents (ID + address proof) requested",
        "Any KYC deficiency notice from the bank",
        "Reference number of the KYC request/complaint",
    ],
    "ombudsman_escalation": [
        "Copy of the complaint first made to the bank",
        "Bank's reply or proof that 30 days have passed",
        "Supporting documents (statements, references, correspondence)",
    ],
    "support_contact_nodal_officer": [
        "Your account/customer ID and complaint reference number",
        "Summary of the issue and dates",
        "Records of prior calls/emails with customer care",
    ],
    "cheque_collection_delay": [
        "Cheque/instrument number, amount and deposit date",
        "Deposit acknowledgement",
        "Any communication about the delay",
    ],
    "deposit_account_service_charge": [
        "Account statement showing the charge",
        "The applicable charges schedule (if available)",
        "Complaint reference number",
    ],
    "deceased_depositor_claim": [
        "Death certificate of the depositor",
        "Nomination details OR legal-heir/succession documents",
        "Your identity proof and relationship proof",
        "Account/deposit details of the deceased",
    ],
    "safe_deposit_locker": [
        "Locker number and locker agreement copy",
        "Rent payment receipts",
        "Details of the issue (access denied, contents, charges)",
    ],
    "loan_complaint": [
        "Loan account number and sanction letter / Key Fact Statement (KFS)",
        "Repayment schedule and statement of account",
        "Any communication about rate/charge changes",
    ],
    "insurance_health_claim": [
        "Policy number and claim number",
        "Hospital bills, discharge summary and prescriptions",
        "Claim rejection/deficiency letter from the insurer/TPA",
    ],
    "insurance_motor_claim": [
        "Policy number and claim number",
        "Vehicle registration, driving licence and FIR (if applicable)",
        "Surveyor report and repair estimate/bills",
    ],
    "insurance_grievance": [
        "Policy number and grievance reference",
        "Copy of the complaint to the insurer and its reply",
        "Supporting documents (claim papers, correspondence)",
    ],
    "unsupported_or_advice_request": [],
}

CATEGORY_LABELS: dict[str, str] = {
    "credit_card_grievance": "Credit Card Grievance",
    "upi_failed_transaction": "UPI Failed Transaction",
    "unauthorized_transaction": "Unauthorized Transaction",
    "failed_transaction_tat": "Failed Transaction TAT / Compensation",
    "kyc_or_identity": "KYC / Identity",
    "ombudsman_escalation": "Ombudsman Escalation",
    "support_contact_nodal_officer": "Support / Nodal Officer",
    "cheque_collection_delay": "Cheque Collection Delay",
    "deposit_account_service_charge": "Deposit Account / Service Charge",
    "deceased_depositor_claim": "Deceased Depositor Claim",
    "safe_deposit_locker": "Safe Deposit Locker",
    "loan_complaint": "Loan Complaint",
    "insurance_health_claim": "Health Insurance Claim",
    "insurance_motor_claim": "Motor Insurance Claim",
    "insurance_grievance": "Insurance Grievance",
    "unsupported_or_advice_request": "Unsupported / Advice Request",
}
