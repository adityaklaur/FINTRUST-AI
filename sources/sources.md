# FinTrust AI Source Registry

Last updated: 2026-07-10

Purpose: This folder contains the first source corpus for FinTrust AI, an MVP for source-grounded financial-services support, grievance, compliance, KYC, risk, and document-intelligence workflows.

Use these files as the initial RAG corpus. The best MVP scope is: credit-card grievances, KYC/identity questions, failed UPI/payment complaints, grievance escalation, Ombudsman escalation, risk classification, and support-response drafting.

Important safety note: These are public documents and public dataset references. Do not use private customer data. Do not present system outputs as legal, financial, regulatory, tax, or banking advice. The product should always show source citations and keep human review in the loop.


## 1. Recommended Ingestion Priority

Start with this order so the first RAG demo becomes useful quickly:

1. `regulatory_rbi/rbi_commercial_banks_credit_debit_card_directions_2025.txt`
2. `regulatory_rbi/rbi_integrated_ombudsman_scheme_2026_faq.txt`
3. `regulatory_rbi/rbi_integrated_ombudsman_scheme_2026_pdf.pdf`
4. `regulatory_rbi/rbi_failed_transactions_tat_compensation_2019` source material: use `rbi_ios_failed_transactions_faq_2021_text.txt` now, and manually re-download the exact RBI notification listed below if needed.
5. `bank_documents/hdfc_credit_card_mitc_english.pdf` and `bank_documents/hdfc_credit_card_mitc_english_extracted.txt`
6. `bank_documents/axis_grievance_redressal_policy_2026.pdf` and extracted text
7. `bank_documents/icici_credit_card_mitc.pdf` and extracted text
8. `bank_documents/sbi_card_customer_grievance_policy.pdf` and extracted text
9. `npci_upi/npci_upi_help_brand_guidelines_2023.pdf`
10. `npci_upi/npci_upi_help_assistant_pilot_2025.pdf`

For the first demo, do not ingest everything at once. Start with 8-12 clean documents, test retrieval quality, then add more.


## 2. Downloaded RBI / Regulatory Sources

### RBI card conduct and grievance documents

- `regulatory_rbi/rbi_commercial_banks_credit_debit_card_directions_2025.txt`
  - Original URL: `https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13155`
  - Use for: credit-card/debit-card grievance redressal, compensation framework, card issuer duties, 30-day escalation to Ombudsman.
  - Notes: Direct `curl` download was blocked by RBI with HTTP 418, so this is a fetched readable text snapshot.

- `regulatory_rbi/rbi_small_finance_banks_credit_debit_card_directions_2025.txt`
  - Original URL: `https://rbi.org.in/SCRIPTS/BS_ViewMasDirections.aspx?id=13123`
  - Use for: same card conduct framework for small finance banks.
  - Notes: Useful if you want broader regulated-entity coverage.

- `regulatory_rbi/rbi_nbfc_credit_card_directions_2025.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12956`
  - Use for: NBFC credit card grievance handling and card issuer duties.

### RBI KYC / AML / CFT documents

- `regulatory_rbi/rbi_kyc_direction_2016_updated_2025.txt`
  - Original URL: `https://www.rbi.org.in/SCRIPTS/BS_ViewMasDirections.aspx?id=11566`
  - Use for: broad KYC/AML/CFT answers, customer due diligence, periodic KYC update, risk-based approach.
  - Notes: This is long. Chunk carefully by sections/headings.

- `regulatory_rbi/rbi_commercial_banks_kyc_directions_2025.txt`
  - Original URL: `https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13141`
  - Use for: commercial-bank-specific KYC/AML/CFT questions.

- `regulatory_rbi/rbi_nbfc_kyc_directions_2025.txt`
  - Original URL: `https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12943`
  - Use for: NBFC-specific KYC/AML/CFT questions.

### RBI Ombudsman and complaint escalation

- `regulatory_rbi/rbi_integrated_ombudsman_scheme_2026_faq.txt`
  - Original URL: `https://www.rbi.org.in/commonperson/English/Scripts/FAQs.aspx?Id=3407`
  - Use for: who can complain, where to complain, CMS portal, CRPC, complaint eligibility, withdrawal, 30-day rule, covered entities.

- `regulatory_rbi/rbi_integrated_ombudsman_scheme_2026_pdf.pdf`
  - Original URL: `https://rbidocs.rbi.org.in/rdocs/content/pdfs/SCHEME16012026_A.pdf`
  - Use for: full official RB-IOS 2026 scheme.
  - Notes: This is one of the most important legal/source documents in the corpus.

- `regulatory_rbi/rbi_ombudsman_scheme_2025_historical_text.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=4749`
  - Use for: historical/contextual comparison only. Do not treat it as the primary current scheme if RB-IOS 2026 applies.

- `regulatory_rbi/rbi_ios_failed_transactions_faq_2021_text.txt`
  - Original URL: RBI FAQ page around Integrated Ombudsman and failed transaction references.
  - Use for: failed transaction escalation context and older FAQ references.
  - Manual follow-up: Try to manually save the exact RBI notification below for the cleanest failed-transaction corpus:
    - `https://www.rbi.org.in/scripts/FS_Notification.aspx?Id=11693&Mode=0&fn=9`
    - Title: `Harmonisation of Turn Around Time (TAT) and customer compensation for failed transactions using authorised Payment Systems`


## 3. Downloaded NPCI / UPI Sources

- `npci_upi/npci_upi_help_brand_guidelines_2023.pdf`
  - Original URL: `https://www.npci.org.in/uploads/UPI_Help_Brand_Guidelines_86c8c28922.pdf`
  - Use for: UPI Help journey, complaint raising, complaint tracking, failed/pending transaction support, fraud note.
  - Good demo questions:
    - "Can UPI Help be used for all transactions?"
    - "Where does the user raise a UPI complaint?"
    - "What should a user do for a fraudulent UPI transaction?"

- `npci_upi/npci_upi_help_brand_guidelines_2023_extracted.txt`
  - Use for: easier text ingestion if PDF parsing is not ready.

- `npci_upi/npci_upi_help_assistant_pilot_2025.pdf`
  - Original URL: `https://www.npci.org.in/uploads/UPI_OC_No_227_FY_2025_26_Introduction_of_UPI_HELP_Assistant_pilot_an_AI_powered_support_for_UPI_payments_cd501de8f3.pdf`
  - Use for: AI-powered UPI Help Assistant pilot, transaction grievance redressal, CRN, participating banks, AI support relevance.

- `npci_upi/npci_upi_chargeback_archive.txt`
  - Original URL: `https://www.npci.org.in/what-we-do/upi/chargeback/archive`
  - Use for: UPI chargeback archive and banking chargeback data context.
  - Notes: Direct `curl` was blocked with 403, so this is a fetched readable text snapshot.

Manual follow-up:

- NPCI circular index:
  - `https://www.npci.org.in/what-we-do/upi/circular`
  - Direct download was blocked with 403.
  - Search manually for `UDIR`, `UPI Help`, `dispute`, `chargeback`, `complaint`, `TAT`, and `grievance`.

- Search terms to use:
  - `site:npci.org.in UDIR UPI complaint circular PDF`
  - `site:npci.org.in UPI chargeback dispute redressal PDF`
  - `site:npci.org.in UPI HELP Assistant pilot AI powered support`


## 4. Downloaded Public Bank Documents

These are useful for simulating real bank policy and complaint workflows. They are not private data.

### HDFC Bank

- `bank_documents/hdfc_credit_card_mitc_english.pdf`
  - Original URL: `https://www.hdfc.bank.in/content/dam/hdfcbankpws/in/en/personal-banking/discover-products/cards/credit-cards/personal-mitc/mitc-in-english.pdf`
  - Use for: HDFC credit-card terms, grievance redressal, contact particulars, compensation framework.

- `bank_documents/hdfc_credit_card_mitc_english_extracted.txt`
  - Use for: text ingestion without PDF parsing.

- `bank_documents/hdfc_credit_card_policy.pdf`
  - Original URL: `https://www.hdfc.bank.in/content/dam/hdfcbankpws/in/en/personal-banking/discover-products/cards-services/credit-card-policy.pdf`
  - Use for: HDFC credit card issuance/conduct policy and grievance process.

- `bank_documents/hdfc_credit_card_policy_extracted.txt`
  - Use for: text ingestion without PDF parsing.

Manual follow-up:

- HDFC grievance redressal policy direct URL was difficult to save reliably with `curl`.
- Search:
  - `HDFC Grievance Redressal Policy Version 1.13 PDF`
  - `site:hdfcbank.com Grievance_Redressal_Policy_Version pdf`

### Axis Bank

- `bank_documents/axis_grievance_redressal_policy_2026.pdf`
  - Original URL: `https://www.axis.bank.in/docs/default-source/default-document-library/grievance-redressal/grievance-redressal-policy.pdf?sfvrsn=3866ba1d_16`
  - Use for: Axis grievance definitions, complaint handling, TAT, failed transaction references.

- `bank_documents/axis_grievance_redressal_policy_2026_extracted.txt`
  - Use for: text ingestion without PDF parsing.

- `bank_documents/axis_credit_card_mitc.pdf`
  - Original URL: `https://www.axisbank.com/docs/default-source/default-document-library/mitc-credit-cards.pdf?sfvrsn=3e341456_8`
  - Use for: Axis credit-card MITC and customer obligations.

- `bank_documents/axis_credit_card_mitc_extracted.txt`
  - Use for: text ingestion without PDF parsing.

- `bank_documents/axis_code_of_commitment.pdf`
  - Original URL: `https://www.axisbank.com/docs/default-source/default-document-library/code-of-commitment.pdf`
  - Use for: complaints, grievance handling, compensation, credit card commitments.

- `bank_documents/axis_code_of_commitment_extracted.txt`
  - Use for: text ingestion without PDF parsing.

- `bank_documents/axis_support_grievance_page.html`
- `bank_documents/axis_support_grievance_page.txt`
  - Original URL: `https://axisbank.com/support`
  - Use for: support/escalation page structure.
  - Note: The HTML/text from direct download is short and may not contain all dynamic website content. Prefer the PDF policies for actual ingestion.

### ICICI Bank

- `bank_documents/icici_credit_card_mitc.pdf`
  - Original URL: `https://www.icicibank.com/content/dam/managed-assets/docs/personal/cards/MITC_cc.pdf`
  - Use for: ICICI credit-card MITC, grievance redressal, customer care, escalation, mis-selling/harassment.

- `bank_documents/icici_credit_card_mitc_extracted.txt`
  - Use for: text ingestion without PDF parsing.

- `bank_documents/icici_customer_grievance_redressal_policy.pdf`
  - Original URL: `https://www.icicibank.com/content/dam/icicibank/managed-assets/docs/complaint/customergrievance-redressal-policy.pdf`
  - Use for: ICICI complaint and grievance redressal policy.

- `bank_documents/icici_feedback_complaint_page.html`
- `bank_documents/icici_feedback_complaint_page.txt`
  - Original URL: `https://www.icicibank.com/feedback`
  - Use for: service request / complaint flow, complaint categories, fraud reporting.

### SBI Card

- `bank_documents/sbi_card_customer_grievance_policy.pdf`
  - Original URL: `https://www.sbicard.com/sbi-card-en/assets/docs/pdf/footer/fair-practice-code/customer-grievance-policy.pdf`
  - Use for: SBI Card grievance principles, escalation, Ombudsman reference, unauthorized transactions.

- `bank_documents/sbi_card_customer_grievance_policy_extracted.txt`
  - Use for: text ingestion without PDF parsing.

- `bank_documents/sbi_card_mitc_english.pdf`
  - Original URL: `https://www.sbicard.com/sbi-card-en/assets/docs/pdf/most-important-terms-and-conditions/English%20MITC.pdf`
  - Use for: SBI Card billing disputes, grievance redressal, chargeback/dispute email references.

- `bank_documents/sbi_card_mitc_english_extracted.txt`
  - Use for: text ingestion without PDF parsing.

- `bank_documents/sbi_card_contact_grievance_page.html`
- `bank_documents/sbi_card_contact_grievance_page.txt`
  - Original URL: `https://www.sbicard.com/en/contact-us/personal.page`
  - Use for: current contact and escalation page context.


## 5. Dataset Metadata and Classification Sources

- `datasets/banking77_readme.txt`
  - Original URL: `https://huggingface.co/datasets/PolyAI/banking77/raw/main/README.md`
  - Use for: understanding BANKING77 structure and license.
  - Important: Direct parquet URLs guessed by automation returned `Entry not found`, so actual data was not downloaded.
  - Recommended loading method later:
    - Python:
      - `pip install datasets`
      - `from datasets import load_dataset`
      - `dataset = load_dataset("PolyAI/banking77")`
  - Use for: banking intent classifier or taxonomy inspiration.

- `datasets/cfpb_huggingface_dataset_card.txt`
  - Original URL: `https://huggingface.co/datasets/CFPB/consumer-finance-complaints/raw/main/README.md`
  - Use for: CFPB dataset metadata, fields, caveats, licensing, and complaint data structure.

Manual follow-up:

- Official CFPB API sample was blocked with Access Denied from this environment.
- Use browser/manual download if needed:
  - `https://www.consumerfinance.gov/data-research/consumer-complaints/`
  - Download CSV from the official site, or use their API locally in a browser/session that is not blocked.
- Suggested for MVP:
  - Do not download the full multi-GB complaint database immediately.
  - Start with 500-2,000 filtered complaint rows for `Credit card`, `Bank account`, `Money transfer`, and `Debt collection`.
  - Remove/avoid any personal information. Use only published public complaint narratives.

Manual search terms:

- `CFPB consumer complaints API download CSV`
- `Hugging Face BANKING77 load_dataset`
- `banking complaint classification dataset Hugging Face`
- `consumer finance complaints credit card CSV sample`


## 6. Research / Architecture References

These are not customer-facing policy documents. Use them to design the product, write README architecture notes, and justify product decisions.

- `research_references/ragas_paper_extracted.txt`
  - Use for: RAG evaluation theory: faithfulness, answer relevance, context relevance/precision.

- `research_references/ragas_metrics_guide_2026.txt`
  - Use for: practical evaluation metrics and thresholds.

- `research_references/genai_engineer_portfolio_guide_2026.txt`
  - Use for: product/portfolio quality expectations around RAG, evaluation, deployment, README.

- `research_references/aws_amazon_finance_regulatory_inquiry_genai.html`
- `research_references/aws_amazon_finance_regulatory_inquiry_genai.txt`
  - Original URL: `https://aws.amazon.com/blogs/machine-learning/how-amazon-finance-streamlines-regulatory-inquiries-by-using-generative-ai-on-aws/`
  - Use for: reference architecture for regulatory inquiry handling using GenAI, RAG, Claude, vector storage, conversation history, observability, and audit trail.

- `research_references/aws_stripe_financial_compliance_agents.html`
- `research_references/aws_stripe_financial_compliance_agents.txt`
  - Original URL: `https://aws.amazon.com/blogs/machine-learning/production-grade-ai-agents-for-financial-compliance-lessons-from-stripe/`
  - Use for: reference architecture for financial compliance agents, human oversight, traceability, and compliance review.

- `research_references/dataiku_ai_explainability_finance.html`
- `research_references/dataiku_ai_explainability_finance.txt`
  - Original URL: `https://www.dataiku.com/blog/ai-explainability-for-financial-services`
  - Use for: explaining auditability, prompt/output logging, retrieved-source tracing, and model governance in finance.

- `research_references/american_express_connectchain_genai_open_source.html`
- `research_references/american_express_connectchain_genai_open_source.txt`
  - Original URL: `https://americanexpress.io/generative-ai-meets-open-source-at-american-express/`
  - Use for: enterprise GenAI orchestration, authentication, authorization, outbound proxy, validation, governance, and security considerations.

- `research_references/langfuse_ragas_eval_guide.html`
- `research_references/langfuse_ragas_eval_guide.txt`
  - Original URL: `https://langfuse.com/guides/cookbook/evaluation_of_rag_with_ragas`
  - Use for: practical RAGAS evaluation and tracing workflow.

- `research_references/ragas_paper_html.html`
- `research_references/ragas_paper_html.txt`
  - Original URL: `https://arxiv.org/html/2309.15217v1`
  - Use for: RAGAS paper in HTML/text form.


## 7. What To Research Next

### Domain workflow

Research:

- How exactly a bank complaint moves from Level 1 support to grievance officer to principal nodal officer to RBI Ombudsman.
- Difference between query, request, complaint, dispute, unauthorized transaction, fraud, failed transaction, and chargeback.
- Which complaint types should be high risk.
- Which answers must be refused because the source corpus is insufficient.

Suggested taxonomy for MVP:

- `credit_card_grievance`
- `fees_or_charges`
- `billing_dispute`
- `failed_transaction`
- `upi_issue`
- `fraud_or_unauthorized_transaction`
- `kyc_or_identity`
- `ombudsman_escalation`
- `support_contact_or_escalation`
- `unsupported_or_advice_request`

### More public documents to add later

Search for:

- RBI Customer Service directions / circulars
- RBI Charter of Customer Rights
- RBI circulars on unauthorized electronic banking transactions
- RBI credit information company grievance rules
- Bank-specific public customer compensation policies
- More official MITC PDFs from Kotak, IDFC First, IndusInd, RBL, HSBC, Standard Chartered
- NPCI UDIR technical/circular documents

Suggested search queries:

- `site:rbi.org.in unauthorized electronic banking transactions customer liability circular`
- `site:rbi.org.in customer service banks grievance compensation master direction`
- `site:rbi.org.in credit information company grievance redressal`
- `site:npci.org.in UDIR complaint resolution UPI circular PDF`
- `site:npci.org.in dispute redressal mechanism UPI PDF`
- `site:hdfcbank.com grievance redressal policy pdf credit card`
- `site:icicibank.com customer grievance redressal policy pdf credit card`
- `site:sbicard.com MITC grievance policy pdf`


## 8. Known Download Issues

- RBI HTML pages returned HTTP 418 to direct `curl`. Readable `.txt` snapshots are saved where available.
- NPCI archive/index pages returned HTTP 403 to direct `curl`. Readable `.txt` snapshots are saved where available.
- HDFC grievance redressal policy direct PDF URL was difficult to save; use manual search/download if this document is critical.
- BANKING77 direct parquet URLs guessed by automation were invalid. Use the Hugging Face `datasets` package instead.
- CFPB API sample was blocked with Access Denied from this environment. Use manual browser download or a local API request later.

Failed-download manifests kept for transparency:

- `curl_batch_regulatory_manifest.json`
- `datasets/dataset_download_manifest.json`


## 9. Suggested First Evaluation Questions

Create 40-50 questions later, but start with these 12:

1. If a credit card complaint is not resolved within 30 days, what can the customer do?
2. What details should a credit card issuer display about the grievance redressal officer?
3. What is the role of the RBI Complaint Management System portal?
4. Can a complainant directly approach the RBI Ombudsman without first approaching the bank?
5. What is UPI Help used for?
6. What should a user do for a suspected fraudulent UPI transaction?
7. What is the purpose of KYC periodic updation?
8. Why do regulated entities use a risk-based approach in KYC/AML?
9. How does HDFC describe grievance redressal for credit card users?
10. What does SBI Card say about escalation to the Nodal Officer?
11. What does ICICI Bank say about credit card grievance escalation?
12. What should the AI do when a question asks for final legal, tax, credit approval, or banking advice not supported by the sources?


## 10. Practical Ingestion Notes

- Prefer `.txt` extracted files first for fast MVP.
- Use PDFs later when your parser is ready and you want page-level citations.
- Keep metadata for every chunk:
  - `source_file`
  - `source_url`
  - `institution`
  - `document_type`
  - `topic`
  - `retrieved_at`
  - `page_or_section` when available
- Chunk long RBI/KYC documents by heading where possible. If using fixed chunks, start with 800-1,200 tokens and 100-150 token overlap.
- Do not mix research-reference articles into the user-facing RAG corpus. Keep them separate from regulatory/bank policy documents.


## 11. Expanded Source Pack Added After Deeper Research

This second source pass adds documents that are highly relevant for a serious product version of FinTrust AI. These sources cover fraud/unauthorized transactions, internal escalation before Ombudsman, customer-service obligations, digital lending complaints, credit information disputes, and more public bank grievance/MITC examples.

### 11.1 High-priority RBI additions

- `regulatory_rbi/rbi_unauthorized_electronic_banking_customer_liability_2017.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/BS_CircularIndexDisplay.aspx?Id=11040`
  - Use for: unauthorized transaction liability, fraud reporting timeline, zero liability, limited liability, shadow reversal, burden of proof.
  - Why it matters: This is essential for fraud/unauthorized-transaction risk classification.
  - Manual PDF URL found but direct download was blocked:
    - `https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/NOTI1506072017.PDF`

- `regulatory_rbi/rbi_unauthorized_electronic_banking_notification_commonman.txt`
  - Original URL: `https://www.rbi.org.in/commonman/English/Scripts/Notification.aspx?Id=2336`
  - Use for: readable RBI commonman version of the same unauthorized electronic banking liability rules.

- `regulatory_rbi/rbi_customer_service_banks_master_circular.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/BS_ViewMasCirculardetails.aspx?Id=6513&Mode=0`
  - Use for: broad customer service obligations, customer grievance redressal policy, customer compensation policy, branch/website disclosures.
  - Why it matters: Helps the system answer non-card banking grievance questions.

- `regulatory_rbi/rbi_internal_ombudsman_regulated_entities_2023.txt`
  - Original URL: `https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12586`
  - Use for: Internal Ombudsman framework across regulated entities.
  - Note: Some 2023 directions have been superseded by 2026 sector-wise directions. Keep this for historical/contextual understanding.

- `regulatory_rbi/rbi_commercial_banks_internal_ombudsman_directions_2026.txt`
  - Original URL: `https://rbi.org.in/SCRIPTS/BS_ViewMasDirections.aspx?id=13271`
  - Use for: bank-level internal escalation before RBI Ombudsman, auto-escalation of partly/wholly rejected complaints, automated complaint management system.
  - Why it matters: This is one of the most important missing pieces for a realistic grievance workflow.

- `regulatory_rbi/rbi_commercial_banks_internal_ombudsman_notification_2026.txt`
  - Original URL: `https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13271&Mode=0`
  - Use for: notification format/version of the commercial bank internal ombudsman directions.

- `regulatory_rbi/rbi_digital_lending_directions_2025_notification.txt`
  - Original URL: `https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12848`
  - Use for: digital lending complaints, Lending Service Provider (LSP) grievance officer, Digital Lending App (DLA), Key Fact Statement (KFS), 30-day escalation to RBI CMS.
  - Why it matters: Makes FinTrust relevant to fintech and loan-app complaint workflows, not only credit cards.

- `regulatory_rbi/rbi_nbfc_digital_lending_directions_2025.txt`
  - Original URL: `https://rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12957`
  - Use for: NBFC digital lending and borrower complaint handling.

- `regulatory_rbi/rbi_credit_information_companies_internal_ombudsman_2026.txt`
  - Original URL: `https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13276`
  - Use for: Credit Information Company internal ombudsman and complaint escalation.

- `regulatory_rbi/rbi_credit_information_compensation_framework_2024.txt`
  - Original URL: `https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12764`
  - Use for: delayed updation/rectification of credit information, Rs. 100/day compensation after 30 calendar days, CI/CIC responsibility.
  - Why it matters: Adds a strong real-world category: credit report/CIBIL correction complaints.

- `regulatory_rbi/rbi_integrated_ombudsman_faq_2021_payment_systems_context.txt`
  - Original URL: `https://www.rbi.org.in/scripts/FAQDisplay.aspx?Id=153`
  - Use for: older RB-IOS payment-system and failed-transaction FAQ context.
  - Note: Use RB-IOS 2026 sources as primary where applicable.

### 11.2 Additional official bank / card documents

These strengthen the institution-specific part of the corpus. They are useful for testing whether the system can distinguish universal RBI rules from individual bank escalation policies.

#### Kotak Mahindra Bank

- `bank_documents/kotak_811_dream_different_kfs_grievance.pdf`
  - Original URL: `https://www.kotak.com/content/dam/Kotak/files/key-fact-statement/811DreamDifferent.pdf`
  - Use for: Kotak KFS/MITC-style grievance escalation, Level 1/2/3 escalation, 30-day Ombudsman escalation.

- `bank_documents/kotak_white_reserve_kfs_grievance.pdf`
  - Original URL: `https://www.kotak.com/content/dam/Kotak/files/key-fact-statement/key-fact-statement-kfs-white-reserve.pdf`
  - Use for: Kotak card terms and grievance escalation.

Manual follow-up:

- Search for a bank-wide Kotak grievance redressal policy PDF:
  - `site:kotak.com grievance redressal policy PDF Kotak Bank`
  - `site:kotak.com credit card MITC PDF grievance redressal`

#### IDFC FIRST Bank

- `bank_documents/idfc_escalation_matrix_tat.pdf`
  - Original URL: `https://www.idfcfirstbank.com/content/dam/idfcfirstbank/grievance-redressal/List-of-escalation-matrix-with-TAT-v2-2.pdf`
  - Use for: escalation matrix, TATs for credit-card disputes, unauthorized transactions, CIBIL/bureau updates, charges/refunds.

- `bank_documents/idfc_credit_card_mitc.pdf`
  - Original URL: `https://www.idfcfirstbank.com/content/dam/idfcfirstbank/pdf/credit-card/MITC-Document-Customer.pdf`
  - Use for: IDFC FIRST credit card MITC and grievance escalation.

- `bank_documents/idfc_credit_card_mitc_extracted.txt`
  - Use for: text ingestion without PDF parser.

- `bank_documents/idfc_credit_card_fees_and_charges_page.txt`
  - Original URL: `https://www.idfcfirstbank.com/content/idfcfirstbank/en/credit-card/fees-and-charges.html`
  - Use for: fee/charges and grievance text snapshot.

#### IndusInd Bank

- `bank_documents/indusind_grievance_redressal_policy_extracted.txt`
  - Original URL: `https://www.indusind.com/content/dam/regulatoryDisclosure/grievanceRedressal/grievance_redressal_policy.pdf`
  - Use for: credit-card grievance levels, 7-working-day internal escalation, head card services, nodal officer.
  - Note: Direct PDF download returned a tiny blocked file, so the text snapshot was saved instead.

- `bank_documents/indusind_mitc_premium_extracted.txt`
  - Original URL: `https://www.indusind.com/content/dam/indusind-corporate/credit-cards/MITC_Premium.pdf`
  - Use for: IndusInd MITC, grievance, contact channels, compensation framework.

#### RBL Bank

- `bank_documents/rbl_credit_card_issuance_conduct_policy.pdf`
  - Original URL: `https://webassets.rblbank.com/document/bank-policies/policy-for-credit-card-issuance-and-conduct.pdf`
  - Use for: RBL credit-card issuance/conduct, dispute transactions, unauthorized use, grievance redressal levels.

- `bank_documents/rbl_credit_card_issuance_conduct_policy_extracted.txt`
  - Use for: text ingestion without PDF parser.

Manual follow-up:

- RBL MITC direct link mentioned inside policy:
  - `https://webassets.rbl.bank.in/document/Credit%20Cards/RBL-MITC-final.pdf`
  - Try manual browser download if needed.

#### YES Bank

- `bank_documents/yesbank_emi_mitc_extracted.txt`
  - Original URL: YES Bank published API PDF URL found during research.
  - Use for: YES Bank credit-card grievance redressal, principal nodal officer, one-month escalation to Banking Ombudsman.
  - Note: Direct PDF download returned a tiny non-PDF placeholder, so text snapshot was saved.

- `bank_documents/yesbank_prosperity_business_credit_cards_mitc_extracted.txt`
  - Use for: YES Bank business credit-card grievance redressal.

- `bank_documents/yesbank_key_fact_statement_extracted.txt`
  - Use for: YES Bank statement/billing dispute instructions and dispute-form reference.

- `bank_documents/yesbank_visa_multicurrency_travel_card_tnc_extracted.txt`
  - Use for: grievance redressal example for non-credit-card card product.

#### Standard Chartered India

- `bank_documents/standard_chartered_grievance_redressal_policy.pdf`
  - Original URL: `https://av.sc.com/in/content/docs/in-updated-grevience-redressal.pdf`
  - Use for: grievance redressal policy, Internal Ombudsman role, grievance redressal day, complaint handling.

Manual follow-up:

- Search individual Standard Chartered India card product pages for MITC PDFs:
  - `site:sc.com/in credit card most important document PDF`
  - `site:sc.com/in credit card terms conditions most important document India`

### 11.3 Community and product-pain research

These are not authoritative policy sources. Do not include them in the answer-grounding corpus unless clearly labelled as non-authoritative research. They are useful for product framing and synthetic/evaluation question creation.

- `research_references/upi_failed_transaction_refund_process_ujjivan_article.txt`
  - Use for: user-language examples around failed UPI payment refunds, T+1/T+5, Rs. 100/day delayed refund compensation.
  - Source type: bank blog / explanatory article, not primary regulation.

Observed pain points from Reddit/Quora/forum-style research:

- Users often do not know whether to contact the app, PSP bank, remitter bank, beneficiary bank, NPCI, or RBI.
- Users are confused about UTR / transaction ID / complaint reference number.
- Support teams often redirect users between app, merchant, bank, and NPCI.
- Many users do not know the 30-day RBI Ombudsman escalation condition.
- Users are unsure when failed-transaction compensation applies.
- Wrong-credit-report/CIBIL complaints are a strong adjacent workflow.

Use this to design:

- synthetic tickets
- evaluation questions
- risk labels
- UI helper text
- "what documents should I attach?" feature
- "where should I escalate next?" workflow

### 11.4 Updated priority for expanded MVP ingestion

For the next serious version, ingest in this order:

1. RBI card conduct directions
2. RBI Integrated Ombudsman 2026 FAQ and PDF
3. RBI unauthorized electronic banking customer liability
4. RBI failed-transaction/TAT material
5. RBI Internal Ombudsman 2026 for commercial banks
6. RBI customer service banks master circular
7. NPCI UPI Help guideline and UPI Help Assistant pilot
8. RBI Digital Lending directions
9. RBI Credit Information Company compensation framework
10. A small subset of bank-specific documents: HDFC, Axis, ICICI, SBI, IDFC, IndusInd, RBL

Do not ingest all bank-specific documents into the first index unless your metadata filtering is ready. Otherwise retrieval may mix bank-specific instructions and produce confusing answers.


## 12. Third Gap-Analysis Source Pack

This final pass found source categories that are not strictly required for the first demo, but are very useful for a serious FinTrust AI product. These make the system more complete across customer rights, wallets/PPIs, collection harassment, payment aggregators, ODR, digital security, account aggregator consent, tokenisation, and complaint-category prioritisation.

### 12.1 Customer rights and complaint taxonomy

- `regulatory_rbi/rbi_committee_review_customer_service_standards_2023.txt`
  - Original URL: `https://www.rbi.org.in/SCRIPTs/PublicationReportDetails.aspx?ID=1232&UrlPage=`
  - Use for: customer-service standards, Charter of Customer Rights discussion, privacy, data protection, grievance redressal, customer service reform ideas.
  - Source type: RBI committee/report reference. Use for product design, not as direct rule text.

- `regulatory_rbi/rbi_customer_rights_and_ombudsman_faq_context.txt`
  - Original source context: RBI customer rights / Ombudsman FAQ material.
  - Use for: Charter of Customer Rights, fair treatment, transparency, suitability, privacy, grievance redressal and compensation.

- `regulatory_rbi/rbi_ombudsman_annual_report_2024_25.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=23441`
  - Use for: complaint category taxonomy and MVP prioritisation.
  - Important insight: top categories include loans and advances, credit cards, mobile/electronic banking, deposit accounts, ATM/debit cards.

- `regulatory_rbi/rbi_ombudsman_annual_report_2023_24.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=23126`
  - Use for: category-wise complaints and year-on-year trends.

- `regulatory_rbi/rbi_ombudsman_annual_report_2022_23.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=22432`
  - Use for: older complaint category trends.

Implementation note:

- Annual reports should not be used to answer individual user complaints.
- Use them to select categories, create dashboards, justify product need, and design evaluation datasets.

### 12.2 PPI / wallet unauthorized transaction sources

- `regulatory_rbi/rbi_ppi_master_direction_unauthorized_transactions_context.txt`
  - Original URL: `https://rbi.org.in/Scripts/NotificationUser.aspx?Id=12156&Mode=0`
  - Use for: PPI/wallet unauthorized electronic payment liability, issuer responsibilities, customer relation policy.

- `regulatory_rbi/rbi_ppi_unauthorized_transaction_faq.txt`
  - Original URL: `https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx?Id=2812`
  - Use for: user-friendly PPI unauthorized transaction FAQ.

- `regulatory_rbi/rbi_ppi_unauthorized_transaction_faq_official.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/FAQView.aspx?Id=126`
  - Use for: official FAQView version of PPI unauthorized transaction FAQ.

Why this matters:

- The first corpus covered bank-account unauthorized transactions, but wallets/PPIs have their own liability rules.
- This matters for Paytm/Amazon Pay/wallet-style complaint flows.

### 12.3 Failed transactions and Online Dispute Resolution

- `regulatory_rbi/rbi_failed_transactions_tat_compensation_2019_clean_extract.txt`
  - Original URL: `https://www.rbi.org.in/commonperson/English/Scripts/Notification.aspx?Id=3074`
  - Use for: clean ingestion of TAT and compensation for failed ATM/card/IMPS/UPI/AEPS/APBS/NACH/PPI transactions.
  - Note: Direct PDF download was blocked, so a clean text extract was saved manually from the RBI web content.

- `regulatory_rbi/rbi_online_dispute_resolution_digital_payments_2020_clean_extract.txt`
  - Original URL: `https://www.rbi.org.in/commonman/English/Scripts/Notification.aspx?Id=3194`
  - Use for: ODR system, TPAP/UPI app dispute lodging, failed transaction complaint tracking, unique reference number.
  - Why this matters: This is very useful for the product workflow because users often ask where to complain first.

- `regulatory_rbi/rbi_ombudsman_2026_atm_failed_transaction_context.txt`
  - Original context: RBI Ombudsman 2026 FAQ with ATM/failed-transaction relevance.
  - Use for: failed ATM transaction plus Ombudsman escalation context.

### 12.4 Recovery, collection, and harassment sources

- `regulatory_rbi/rbi_credit_card_operations_master_circular_recovery_agents_context.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/BS_ViewMasCirculardetails.aspx?id=7338`
  - Use for: recovery agents, harassment, intimidation, humiliation, credit-card collection complaint context.

- `regulatory_rbi/rbi_nbfc_responsible_business_conduct_recovery_fpc.txt`
  - Original URL: `https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12942`
  - Use for: NBFC fair practices, KFS, grievance mechanism, recovery harassment restrictions.

- `regulatory_rbi/rbi_nbfc_recovery_agents_conduct_historical_2025.txt`
  - Original URL: `https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=5036`
  - Use for: NBFC recovery-agent conduct, harsh recovery practices, recovery-related grievance mechanism.

- `regulatory_rbi/rbi_banks_recovery_agents_conduct_historical_2025.txt`
  - Original URL: `https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=5029`
  - Use for: bank recovery-agent conduct, harassment, privacy intrusion, grievance officer disclosure.

- `regulatory_rbi/rbi_nbfc_fair_practices_kfs_recovery_direction.txt`
  - Original URL: `https://rbi.org.in/SCRIPTs/BS_ViewMasDirections.aspx?id=12942`
  - Use for: NBFC Fair Practices Code, Key Facts Statement, recovery conduct, grievance mechanism.

- `regulatory_rbi/rbi_nbfc_faq_grievance_fair_practices.txt`
  - Original URL: `https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=1167`
  - Use for: NBFC complaint/grievance context in simpler FAQ style.

Why this matters:

- Loan recovery harassment is a major real-world complaint area.
- This should be a high-risk category in the classifier.
- The assistant should avoid giving legal conclusions; it should explain complaint routes and required evidence.

### 12.5 Payment aggregators and dispute management

- `regulatory_rbi/rbi_payment_aggregators_guidelines_2020.txt`
  - Original URL: `https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=11822&Mode=0`
  - Use for: payment aggregator complaint/dispute/refund responsibilities, nodal officer, refund timelines, dispute management framework.

- `regulatory_rbi/rbi_payment_aggregators_master_directions_2024.txt`
  - Original URL: `https://www.rbi.org.in/SCRIPTs/BS_ViewMasDirections.aspx?id=12896`
  - Use for: payment aggregator master directions, dispute framework, chargebacks, reason codes, merchant/payment roles.

- `regulatory_rbi/rbi_payment_aggregator_ombudsman_context.txt`
  - Use for: connecting PA complaints with RBI Ombudsman context.

Why this matters:

- Many failed transactions involve merchant/acquirer/payment aggregator ambiguity.
- The system can ask: Did you pay a merchant? Which app? Which bank? Do you have merchant confirmation?

### 12.6 Digital security, tokenisation, and consent sources

- `regulatory_rbi/rbi_cyber_resilience_payment_security_controls_pso_2024.txt`
  - Original URL: `https://rbi.org.in/SCRIPTs/BS_ViewMasDirections.aspx?id=12715`
  - Use for: cyber resilience and digital payment security controls for non-bank payment system operators.

- `regulatory_rbi/rbi_digital_payment_security_controls_2020.txt`
  - Original URL: `https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12032`
  - Use for: security controls for mobile/internet banking, fraud marking, authentication, secure digital payment environment.

- `regulatory_rbi/rbi_card_tokenisation_faq_2026_context.txt`
  - Original URL context: RBI tokenisation FAQ.
  - Use for: tokenisation consent, AFA, whether tokenisation is mandatory, who to contact for tokenised-card issues or device loss.

- `regulatory_rbi/rbi_credit_card_grievance_older_notification_context.txt`
  - Original URL: `https://www.rbi.org.in/commonperson/english/scripts/Notification.aspx?Id=1443`
  - Use for: older credit-card grievance redressal and complaint acknowledgement context.
  - Note: Use current 2025 directions as primary.

### 12.7 Account Aggregator, consent, privacy, and KYC update sources

- `regulatory_rbi/rbi_account_aggregator_directions_2016.txt`
  - Original URL: `https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=10598`
  - Use for: Account Aggregator consent artefact, no credential storage, customer grievance handling, right to revoke/complain.

- `regulatory_rbi/rbi_nbfc_account_aggregator_directions_2025.txt`
  - Original URL: `https://rbi.org.in/SCRIPTs/BS_ViewMasDirections.aspx?id=12936`
  - Use for: updated NBFC-AA grievance, consent, privacy, customer data sharing.

- `regulatory_rbi/rbi_account_aggregator_notification_2016.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=10598`
  - Use for: notification version of Account Aggregator directions.

- `regulatory_rbi/rbi_commercial_banks_kyc_directions_2025_second_snapshot.txt`
  - Use for: CKYCR / KYC update / periodic updation context.

Why this matters:

- These are stretch sources, but useful if FinTrust later handles privacy, consent, KYC update, or financial-data-sharing complaints.

### 12.8 Manual-only sources still worth fetching

If you want an even more complete corpus, manually fetch these:

1. RBI Charter of Customer Rights original / model customer rights policy
   - Search: `RBI Charter of Customer Rights PDF Model Customer Rights Policy`

2. RBI Customer Protection PDF for unauthorized electronic banking
   - URL found but direct download blocked:
   - `https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/NOTI1506072017.PDF`

3. RBI TAT failed transaction PDF
   - URL found but direct download blocked:
   - `https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/CIRCULAR677EC931A7A65E4D99AA957D8E85BC0A2A.PDF`
   - Clean extract already saved, so manual PDF is optional.

4. RBI Financial Literacy grievance redress PDF
   - URL found but direct download blocked:
   - `https://www.rbi.org.in/commonman/Upload/english/Content/PDFs/Grievance%20Redress.pdf`

5. Payment aggregator official FAQs or individual PA grievance policies
   - Search: `Razorpay grievance redressal policy payment aggregator RBI`, `Cashfree grievance redressal policy`, `PayU nodal officer grievance`

6. Official card-network dispute/chargeback public rules
   - Visa/Mastercard/RuPay public dispute material may be useful but may not be fully public.
   - Search: `RuPay dispute chargeback rules public PDF NPCI`, `Visa chargeback dispute public guide India`.

7. More bank policies
   - HSBC India, Federal Bank, Bank of Baroda, Canara Bank, PNB, AU Small Finance Bank, IDBI, Union Bank, etc.

### 12.9 Updated expanded classifier categories

Add these categories to the earlier taxonomy when you build the classifier:

- `unauthorized_transaction_bank_account`
- `unauthorized_transaction_ppi_wallet`
- `failed_transaction_tat_compensation`
- `upi_odr_or_app_dispute`
- `payment_aggregator_merchant_refund`
- `recovery_agent_harassment`
- `loan_kfs_or_hidden_charges`
- `digital_lending_lsp_complaint`
- `credit_information_cibil_correction`
- `account_aggregator_consent_privacy`
- `card_tokenisation_or_device_loss`
- `customer_rights_or_privacy`

For MVP, still start smaller:

- credit-card grievance
- failed UPI/payment transaction
- unauthorized transaction
- KYC issue
- Ombudsman escalation
- support contact / nodal officer
- unsupported/advice request


## 13. Insurance Expansion Source Pack

Insurance can be covered, but it should be treated as a separate expansion module. It has a different regulator, different grievance path, and different source authority:

- Banking / payments: RBI, NPCI, banks, payment operators
- Insurance: IRDAI, Bima Bharosa, Council for Insurance Ombudsmen, insurers, policy wordings

Recommended product label if insurance is included:

- `FinTrust AI - Banking, Payments and Insurance Claims Copilot`
- Or keep the first product banking-only and create a separate tab: `Insurance Claims`

Do not mix these documents into the same vector collection without metadata filtering. Use at least:

- `domain = banking_payments`
- `domain = insurance`
- `insurance_type = health | life | motor | property | grievance`
- `authority = IRDAI | Insurance Ombudsman | insurer`

### 13.1 Insurance ingestion priority

If you want to add insurance, ingest in this order:

1. `insurance_irdai/irdai_policyholders_interests_claims_grievance_2024.txt`
2. `insurance_irdai/insurance_ombudsman_rules_2017.txt`
3. `insurance_irdai/irdai_health_insurance_handbook_cashless_reimbursement.txt`
4. `insurance_irdai/irdai_health_insurance_regulations_2012_claims_cashless.txt`
5. `insurance_irdai/irdai_standardization_exclusions_health_insurance.txt`
6. `insurance_irdai/irdai_standard_term_life_saral_jeevan_guidelines.txt`
7. `insurance_irdai/irdai_policyholder_claim_guidance_motor_health_life_property.txt`
8. `insurance_irdai/irdai_bharat_griha_raksha_guidelines.txt`
9. `insurance_irdai/irdai_bharat_griha_raksha_standard_wording_annexure.txt`
10. One or two insurer-specific examples only, such as Arogya Sanjeevani or Saral Jeevan Bima examples.

### 13.2 Core insurance policyholder and grievance sources

- `insurance_irdai/irdai_policyholders_interests_claims_grievance_2024.txt`
  - Source: IRDAI policyholder protection / claims / grievance regulation material.
  - Use for: claim settlement, policyholder treatment, required documents at one go, grievance redressal, insurer obligations.
  - Why it matters: This is the insurance equivalent of the RBI customer-protection source layer.

- `insurance_irdai/irdai_protection_policyholders_interests_regulations_2024_draft.txt`
  - Source: IRDAI Protection of Policyholders' Interests and Allied Matters of Insurers Regulations, 2024 draft/reference material.
  - Use for: policyholder-centric governance, free-look period, servicing, claim settlement, grievance redressal.
  - Note: Prefer final/official versions when manually downloaded.

- `insurance_irdai/insurance_ombudsman_rules_2017.txt`
  - Source: Insurance Ombudsman Rules, 2017.
  - Use for: who can approach Insurance Ombudsman, claim delay, claim repudiation, premium dispute, policy servicing grievance, complaint format, one-year condition, one-month insurer response condition.

Manual follow-up:

- Bima Bharosa FAQ / complaint portal:
  - `https://bimabharosa.irdai.gov.in/Home/FAQ`
  - `https://bimabharosa.irdai.gov.in/`
- IRDAI Grievance Cell:
  - `https://irdai.gov.in/en/web/guest/grievance-cell-cad`
- Council for Insurance Ombudsmen:
  - `https://www.cioins.co.in/`

### 13.3 Health insurance, cashless, reimbursement, OPD and exclusions

- `insurance_irdai/irdai_health_insurance_master_circular_2024_document_page.txt`
  - Source: IRDAI document detail for Master Circular on Health Insurance Business, 2024.
  - Use for: locating official master circular and annexure.
  - Manual follow-up: Download actual English PDF and annexure from IRDAI document page:
    - `https://irdai.gov.in/en/document-detail?documentId=4942918`

- `insurance_irdai/irdai_health_insurance_product_filing_cis_guidelines.txt`
  - Use for: Customer Information Sheet (CIS), policy benefits, exclusions, claim process summary, sublimits.

- `insurance_irdai/irdai_health_insurance_regulations_2012_claims_cashless.txt`
  - Use for: cashless definition, network provider, claim settlement within 30 days of complete documents, identity card for cashless facility, TPA/network provider context.

- `insurance_irdai/irdai_health_insurance_handbook_cashless_reimbursement.txt`
  - Use for: simple health insurance explanation, cashless facility, reimbursement, network hospital, non-network hospital.

- `insurance_irdai/irdai_standardization_exclusions_health_insurance.txt`
  - Use for: standardized exclusions, pre-existing disease exclusion code, waiting period, investigation/evaluation, rest cure, obesity, cosmetic surgery, hazardous sports, breach of law, unproven treatments.

- `insurance_irdai/arogya_sanjeevani_policy_wording_bajaj_example.txt`
  - Use for: standard health policy example, exclusions, co-pay, claim handling.

- `insurance_irdai/arogya_sanjeevani_sbi_health_cis_policy_example.txt`
  - Use for: CIS-style example, exclusions, claims, waiting periods.

- `insurance_irdai/icici_lombard_group_health_cis_example.txt`
  - Use for: group health CIS example, cashless/reimbursement flow and claim documents.

Insurance feature ideas from these sources:

- Explain cashless vs reimbursement.
- Tell user which documents may be needed.
- Identify whether OPD is generally excluded unless specifically covered.
- Explain pre-existing disease waiting period, but always cite specific policy wording.
- Refuse to decide claim admissibility without policy wording and facts.

### 13.4 Term / life insurance sources

- `insurance_irdai/irdai_standard_term_life_saral_jeevan_guidelines.txt`
  - Use for: standard term life product, Saral Jeevan Bima, death benefit, waiting period, death claim documents.

- `insurance_irdai/saral_jeevan_bima_sud_life_policy_example.txt`
- `insurance_irdai/saral_jeevan_bima_max_life_policy_example.txt`
- `insurance_irdai/saral_jeevan_bima_canara_hsbc_policy_example.txt`
- `insurance_irdai/saral_jeevan_bima_abslife_policy_example.txt`
  - Use for: insurer-specific policy wording examples.
  - Important: These are examples, not universal answers for every life insurance policy.

Insurance feature ideas:

- Death claim document checklist.
- Explain nominee/assignee/legal heir claim basics.
- Explain Saral Jeevan Bima 45-day waiting period.
- Ask for policy type, policy start date, death date, cause of death, nominee status, and documents available.

### 13.5 Motor / car insurance sources

- `insurance_irdai/irdai_policyholder_claim_guidance_motor_health_life_property.txt`
  - Source: IRDAI policyholder claim guidance page snapshot.
  - Use for: motor, life, health, property claim guidance.

- `insurance_irdai/motor_insurance_claim_settlement_policy_example.txt`
  - Use for: motor claim settlement timeline example, 30-day settlement/rejection after necessary documents or survey report.

Motor feature ideas:

- Own damage vs third-party claim explanation.
- Theft claim checklist: police intimation, insurer intimation, keys, non-traceable certificate.
- Accident claim checklist: do not move vehicle without required permission, inform insurer/police, RC, repair estimate, invoice, receipts.
- Cashless garage vs reimbursement.

Manual follow-up:

- IRDAI Motor Insurance Handbook:
  - Search: `IRDAI Motor Insurance Handbook English PDF`
- IRDAI "How to Make a Claim - Motor":
  - `https://irdai.gov.in/en/web/policy-holder/how-to-make-a-claim-motor`

### 13.6 Property / home insurance sources

- `insurance_irdai/irdai_bharat_griha_raksha_guidelines.txt`
  - Use for: standard home insurance product guidelines, Bharat Griha Raksha, fire and allied perils.

- `insurance_irdai/irdai_bharat_griha_raksha_standard_wording_annexure.txt`
  - Use for: standard policy wording, insured events, exclusions, policy schedule, home building/contents cover.

- `insurance_irdai/bharat_griha_raksha_united_policy_wording_example.txt`
  - Use for: insurer-specific Bharat Griha Raksha example.

- `insurance_irdai/irdai_property_insurance_handbook_claims_grievance.txt`
  - Use for: property claim education, grievance route, insurer first then IRDAI/IGMS.

- `insurance_irdai/property_insurance_claim_procedure_example.txt`
  - Use for: property claim procedure, immediate notice, claim form within 30 days, surveyor, proof of loss.

Property feature ideas:

- Fire/flood/home damage claim checklist.
- Ask if police/fire brigade/local authority report is needed.
- Ask for policy schedule, photos, proof of loss, repair estimate, surveyor communication.
- Explain that policy wording and exclusions control the final answer.

### 13.7 Insurance classifier categories

If insurance is added, add these categories:

- `insurance_health_cashless`
- `insurance_health_reimbursement`
- `insurance_health_opd_or_exclusion`
- `insurance_health_pre_existing_waiting_period`
- `insurance_life_death_claim`
- `insurance_life_waiting_period`
- `insurance_motor_own_damage`
- `insurance_motor_third_party`
- `insurance_motor_theft`
- `insurance_property_home_damage`
- `insurance_claim_rejection_or_repudiation`
- `insurance_grievance_irdai_bima_bharosa`
- `insurance_ombudsman_escalation`

### 13.8 Important scope warning

Insurance expansion is valuable, but it can make the product too broad if added too early.

Recommended approach:

- MVP 1: Banking/payments grievance copilot.
- MVP 2: Insurance claims and grievance copilot.
- Later: Unified financial services trust copilot with domain filters.

Never answer insurance questions from banking documents or banking questions from insurance documents. Metadata filtering is mandatory.


## 14. Additional Bank-Focused Source Pack

This pass adds broader retail-banking documents that are useful beyond credit-card and UPI complaints. These sources improve coverage for deposit accounts, service charges, cheque clearing, RTGS/NEFT, safe deposit lockers, deceased depositor claims, debit cards, and bank-specific compensation policies.

### 14.1 RBI retail-banking customer service and deposit account sources

- `regulatory_rbi/rbi_customer_service_banks_master_circular_deposit_accounts.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/BS_ViewMasCirculardetails.aspx?id=7363`
  - Use for: deposit account operation, service charges, grievance policies, customer compensation policy, customer service.

- `regulatory_rbi/rbi_customer_service_urban_cooperative_banks_master_circular_context.txt`
  - Original URL: `https://www.rbi.org.in/commonperson/English/Scripts/Notification.aspx?Id=1588`
  - Use for: customer service and deposit account context in UCBs; useful as supporting material.

- `regulatory_rbi/rbi_commercial_banks_deposit_accounts_service_charges_2025.txt`
  - Original URL: `https://rbi.org.in/SCRIPTS/BS_ViewMasDirections.aspx?id=13140`
  - Use for: commercial bank deposit accounts, minimum balance, account closure charges, service charges, inoperative accounts, customer relations policy.

- `regulatory_rbi/rbi_payments_banks_deposit_accounts_service_charges_2025.txt`
  - Original URL: `https://www.rbi.org.in/SCRIPTS/BS_ViewMasDirections.aspx?id=13089`
  - Use for: payments bank deposit accounts and service-charge framework.

Why these matter:

- Many real complaints are not credit-card complaints. They are about account closure charges, minimum balance charges, deposit account servicing, inoperative accounts, and service-charge disclosure.

### 14.2 Cheque collection and clearing delay sources

- `regulatory_rbi/rbi_master_circular_customer_service_cheque_collection_2012.txt`
  - Original URL: `https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/50MC020712SF.pdf`
  - Use for: cheque collection policy, customer compensation policy, grievance redressal, delayed cheque clearing.

- `regulatory_rbi/rbi_master_circular_customer_service_cheque_collection_2015.txt`
  - Original URL: `https://rbi.org.in/Scripts/BS_ViewMasCirculardetails.aspx?id=9862`
  - Use for: updated customer-service master circular with cheque collection and compensation references.

- `regulatory_rbi/rbi_cheque_collection_delay_compensation_context.txt`
  - Original URL: `https://www.rbi.org.in/commonperson/English/Scripts/Notification.aspx?Id=1588`
  - Use for: local/outstation cheque delay compensation and requirement to pay interest for delay.

Useful classifier categories:

- `cheque_collection_delay`
- `cheque_return_or_stop_payment`
- `service_charge_or_account_fee`

### 14.3 RTGS / NEFT / IMPS / payment-system FAQ sources

- `regulatory_rbi/rbi_rtgs_neft_failed_transaction_faq_context.txt`
  - Original source: RBI RTGS/NEFT FAQ material.
  - Use for: RTGS/NEFT dispute handling, compensation for delayed return, grievance escalation.

- `regulatory_rbi/rbi_payment_system_failed_transaction_faq_context.txt`
  - Original source: RBI failed-payment-system FAQ context.
  - Use for: IMPS/UPI/NEFT/RTGS failed transactions and RB-IOS escalation context.

Implementation note:

- For NEFT/RTGS questions, do not blindly apply UPI T+1/T+5 rules. Use NEFT/RTGS-specific FAQ or RBI payment-system circulars.

### 14.4 Safe deposit locker and deceased customer claim sources

- `regulatory_rbi/rbi_safe_deposit_locker_direction_context.txt`
  - Original URL: `https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13063`
  - Use for: safe deposit locker agreement, bank liability, illegal/hazardous content clause, locker access and compensation.

- `regulatory_rbi/rbi_safe_deposit_locker_notification_2021.txt`
  - Original URL: `https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12146`
  - Use for: safe deposit locker revised instructions, Supreme Court context, bank duty of care.

- `regulatory_rbi/rbi_deceased_customer_claims_safe_deposit_locker_2025.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12901&Mode=0`
  - Use for: deceased customer claims, deposit accounts, safe deposit lockers, articles in safe custody, compensation for delay.

- `regulatory_rbi/rbi_deceased_customer_claims_notification_2025.txt`
  - Original URL: `https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12901&Mode=0`
  - Use for: same as above, alternate notification capture.

- `regulatory_rbi/rbi_deceased_customer_claims_historical_2025.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=4698`
  - Use for: historical/document view of deceased customer claim directions.

- `regulatory_rbi/rbi_settlement_claims_deceased_depositors_older_context.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/NotificationUser.aspx?Mode=0&id=6552`
  - Use for: older settlement of deceased depositor claim context.

Useful classifier categories:

- `safe_deposit_locker_access_or_loss`
- `deceased_depositor_claim`
- `nominee_or_legal_heir_claim`

### 14.5 Added bank-specific compensation and depositor-rights sources

These are useful for institution-specific answers. Do not use them as universal rules.

#### HDFC Bank

- `bank_documents/hdfc_purchase_card_mitc_compensation_context.txt`
  - Use for: HDFC purchase card MITC, compensation policy references, failed/unsuccessful transaction and grievance redressal context.

Manual follow-up:

- HDFC Customer Compensation Policy PDF was identified:
  - `https://www.hdfcbank.com/content/bbp/repositories/723fb80a-2dde-42a3-9793-7ae1be57c87f/?path=%2FCommon+Overlays%2FFeedback%2FPDFS%2FCitizens+Charter%2Fcustomer-compensation-Policy-June-25.pdf`
  - Direct save may be blocked/dynamic. Manually download if you want the PDF.

#### Axis Bank

- `bank_documents/axis_grievance_redressal_policy_compensation_context.txt`
  - Use for: Axis grievance redressal policy with failed transaction TAT and compensation context.

- `bank_documents/axis_debit_card_mitc_grievance_compensation.txt`
  - Use for: Axis debit card MITC, grievance redressal, unauthorized transaction and dispute timelines.

- `bank_documents/axis_code_of_commitment_compensation_context.txt`
  - Use for: Axis code of commitment, compensation and grievance handling commitments.

#### ICICI Bank

- `bank_documents/icici_credit_card_mitc_web_terms_dispute_context.txt`
  - Use for: ICICI credit card web MITC, billing disputes, failed/reversed transactions, escalation.

Manual follow-up:

- ICICI customer-service policies page lists useful PDFs:
  - `https://www.icicibank.com/customer-service-policies`
  - Documents to manually download:
    - Grievance Redressal Policy
    - Cheque Collection Policy
    - Policy on Collection of Dues and Repossession of Security
    - Customer Rights Policy
    - Deposit Policy
    - Customer Relations Policy
    - Compensation Policy
    - Deceased Depositors Policy

#### SBI / State Bank of India

- `bank_documents/sbi_customer_rights_grievance_compensation_policy_2023.txt`
  - Original URL: official SBI PDF found via `sbi.co.in`.
  - Use for: SBI customer rights, grievance redressal, compensation policy, failed transactions, unauthorized/erroneous debit.

- `bank_documents/sbi_policy_on_depositors_rights_2025.txt`
  - Original URL: official SBI depositor rights policy.
  - Use for: depositor rights, ATM failure, compensation, grievance redressal.

#### Kotak Mahindra Bank

- `bank_documents/kotak_grievance_redressal_policy.txt`
  - Original URL: `https://www.kotak.com/content/dam/Kotak/Customer-Service/Important-Customer-Information/Banking-Policies/policy-for-grievance-redressal.pdf`
  - Use for: Kotak grievance redressal process, TAT categories, escalation.

#### IDFC FIRST Bank

- `bank_documents/idfc_grievance_redressal_policy.txt`
  - Original URL: `https://www.idfcfirstbank.com/content/dam/idfcfirstbank/grievance-redressal/Grievance-Redressal.pdf`
  - Use for: IDFC grievance policy, ATM failed transaction compensation, unauthorized transaction shadow reversal, 90-day resolution.

- `bank_documents/idfc_general_terms_grievance_context.txt`
  - Original URL: `https://www.idfcfirstbank.com/content/dam/idfcfirstbank/pdf/IDFC-FIRST-Bank-General-Terms-and-Conditions.pdf`
  - Use for: general terms, grievance channels, escalation to regulator.

### 14.6 Updated banking classifier categories

Add these categories if you want broader banking coverage:

- `deposit_account_service_charge`
- `minimum_balance_or_account_closure_charge`
- `inoperative_account_or_kyc_reactivation`
- `cheque_collection_delay`
- `cheque_return_or_stop_payment`
- `neft_rtgs_imps_failed_transfer`
- `atm_cash_not_dispensed`
- `debit_card_dispute`
- `safe_deposit_locker_access_or_loss`
- `deceased_depositor_nominee_claim`
- `bank_customer_compensation_policy`

### 14.7 Implementation warning

This broader bank corpus is powerful but can confuse retrieval if all documents are mixed without metadata filters.

Recommended metadata:

- `domain = banking_payments`
- `subdomain = credit_card | deposit_account | payment_transfer | cheque | locker | deceased_claim | debit_card | bank_compensation`
- `authority = RBI | bank`
- `institution = hdfc | axis | icici | sbi | kotak | idfc | general`

For the first implementation, use filters:

- If user asks about a specific bank, search that bank's documents plus RBI.
- If user does not specify a bank, search RBI/general regulatory sources first.
- Never answer a general RBI question from one bank's compensation policy unless clearly labelled as institution-specific.


## 15. Final Bank Implementation Source Pack

This pass adds sources that are especially useful for implementation and model training because they create realistic categories beyond credit card, UPI, and generic grievance. These include loans, BBPS, NACH/autopay, AePS, unclaimed deposits, deposit insurance, vulnerable-customer banking, fraud awareness, and unauthorized deposit scheme reporting.

### 15.1 Loan servicing, penal charges, KFS and floating EMI reset

- `regulatory_rbi/rbi_fair_lending_penal_charges_loan_accounts_2023.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12527`
  - Use for: penal charges in loan accounts, no capitalization of penal charges, clear disclosure in loan agreement and KFS.

- `regulatory_rbi/rbi_penal_charges_loan_accounts_faq_context.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/FAQView.aspx?Id=162`
  - Use for: FAQ-style clarifications on penal charges.

- `regulatory_rbi/rbi_housing_finance_master_circular_floating_rate_context.txt`
  - Original URL: `https://www.rbi.org.in/Scripts/BS_ViewMasterCirculars.aspx?Id=12824&Mode=0`
  - Use for: housing finance context and link to floating-rate EMI reset instructions.

Manual follow-up:

- Floating-rate EMI reset full FAQ PDF:
  - Search: `RBI FAQ reset floating interest rate EMI personal loans PDF`
  - Useful topics: communication of EMI/tenor change, quarterly statements, option to increase EMI/extend tenor/switch fixed rate where offered.

Classifier categories:

- `loan_penal_charges`
- `loan_kfs_or_apr_disclosure`
- `floating_rate_emi_reset`
- `home_loan_prepayment_or_tenor_issue`

### 15.2 BBPS, NACH, AePS and payment-system disputes

- `regulatory_rbi/rbi_bbps_guidelines_complaint_management_2014.txt`
  - Original URL: `https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/BBPSTG28112014.pdf`
  - Use for: BBPS complaint management, unique complaint reference number, customer service disclosure, centralized ticketing.

- `regulatory_rbi/rbi_bbps_ombudsman_payment_system_context.txt`
  - Use for: BBPS and payment-system Ombudsman context.

- `regulatory_rbi/rbi_nach_mandate_revocation_failed_transaction_context.txt`
  - Use for: NACH mandate revocation, account debited despite revoked mandate, T+1 resolution.

Already relevant existing source:

- `regulatory_rbi/rbi_failed_transactions_tat_compensation_2019_clean_extract.txt`
  - Contains AePS, APBS, NACH, UPI, IMPS, cards and ATM failed transaction TAT.

Classifier categories:

- `bbps_bill_payment_dispute`
- `nach_autopay_mandate_dispute`
- `aeps_failed_transaction`
- `apbs_or_nach_credit_delay`

### 15.3 UDGAM, unclaimed deposits and DICGC deposit insurance

- `regulatory_rbi/rbi_udgam_unclaimed_deposits_portal_notes.txt`
  - Source URLs: UDGAM portal, RBI UDGAM FAQs, DEA Fund FAQs.
  - Use for: unclaimed deposit search, UDRN, DEA Fund, claim through respective bank, legal heir/nominee routing.

- `regulatory_rbi/rbi_fame_financial_awareness_unclaimed_deposits_fraud.txt`
  - Use for: financial awareness messages about unclaimed deposits and UDGAM.

- `regulatory_rbi/dicgc_deposit_insurance_faq.txt`
  - Original URL: `https://www.dicgc.org.in/FAQs`
  - Use for: deposit insurance up to Rs. 5 lakh per depositor per bank, liquidation/AID/amalgamation payout process.

Manual follow-up:

- DICGC information booklet:
  - `https://www.dicgc.org.in/sites/default/files/2025-02/dicgc-information-booklet.pdf`
- RBI DICGC FAQ:
  - Search: `RBI DICGC FAQ deposit insurance 5 lakh`

Classifier categories:

- `unclaimed_deposit_udgam`
- `dea_fund_claim`
- `dicgc_deposit_insurance`
- `bank_under_restriction_or_liquidation`

### 15.4 Senior citizens, differently-abled and accessibility banking

- `regulatory_rbi/rbi_senior_citizens_differently_abled_doorstep_banking_context.txt`
  - Original source: RBI doorstep banking directions/context.
  - Use for: doorstep banking for senior citizens over 70, differently abled/infirm persons, KYC/life certificate/cash pickup/delivery.

- `regulatory_rbi/rbi_senior_differently_abled_ombudsman_faq_context.txt`
  - Use for: FAQ/Ombudsman context for senior/differently-abled banking service complaints.

- `regulatory_rbi/rbi_visually_impaired_banking_facilities_context.txt`
  - Use for: visually impaired customers' access to cheque book, ATM, locker, internet banking, loans, cards without discrimination.

- `regulatory_rbi/rbi_visually_impaired_talking_atm_context.txt`
  - Use for: talking ATMs, Braille keypads, low-vision support, branch magnifying glasses.

Classifier categories:

- `senior_citizen_doorstep_banking`
- `differently_abled_banking_access`
- `visually_impaired_banking_facility_denial`
- `life_certificate_or_pension_service`

### 15.5 Fraud awareness and Sachet unauthorized deposit reporting

- `regulatory_rbi/rbi_fame_financial_awareness_fraud_upi_customer_liability.txt`
  - Source: RBI Financial Awareness Messages.
  - Use for: fraud awareness, UPI/customer liability, never share OTP/PIN/password, reporting fraud quickly.

- `regulatory_rbi/rbi_sachet_unauthorized_deposits_portal_notes.txt`
  - Source URLs: `https://sachet.rbi.org.in/home`, `https://sachet.rbi.org.in/FAQ/FAQ`
  - Use for: unauthorized deposit schemes, Ponzi/MLM/fake investment schemes, illegal money collection, routing to Sachet instead of RBI CMS.

Manual follow-up:

- BE(A)WARE booklet PDF:
  - `https://rbidocs.rbi.org.in/rdocs/content/pdfs/BEAWARE07032022.pdf`
  - Direct PDF was identified; manually download if you want the original booklet.

Classifier categories:

- `phishing_or_otp_fraud_awareness`
- `upi_scam_or_social_engineering`
- `unauthorized_deposit_or_investment_scheme`
- `sachet_or_rbi_cms_routing`

### 15.6 Final high-value bank categories now covered

After this pass, the corpus has useful source coverage for:

- Credit cards
- Debit cards
- UPI
- IMPS
- NEFT / RTGS
- ATM / cash not dispensed
- AePS / APBS / NACH
- BBPS bill payments
- Deposit account service charges
- Inoperative accounts
- Unclaimed deposits
- Deceased depositor claims
- Safe deposit lockers
- Cheque collection delays
- Loan KFS / APR / penal charges
- Floating EMI reset
- Digital lending complaints
- Recovery harassment
- Credit information / CIC complaints
- DICGC deposit insurance
- Senior citizen and differently-abled banking
- Fraud awareness and unauthorized deposit scheme reporting

### 15.7 Implementation advice

At this point, do not keep collecting forever. The corpus is already large enough to start building.

Recommended implementation order:

1. Build ingestion and metadata registry.
2. Build a small RBI-only index with 10-15 core documents.
3. Add bank-specific documents only after metadata filters work.
4. Add broad categories gradually: card, UPI, unauthorized transaction, deposits, cheque, locker, loans, insurance.
5. Create evaluation sets category by category.

Important:

- A bigger corpus does not automatically mean better answers.
- Retrieval quality will depend on metadata, chunking, source ranking, and refusal logic.
- Use `sources.md` as the source-of-truth registry for metadata design.


## 16. P0 Pending Source Acquisition Status

This section records the first step of the pending-source acquisition plan from `FinTrust_AI_Project_Proposal.txt`.

Status labels:

- `Acquired - PDF`: original/stable PDF downloaded.
- `Acquired - clean extract`: direct PDF was blocked or not easily downloadable, but a clean source extract was saved.
- `Acquired - snapshot`: reliable text snapshot saved from official source/search fetch.
- `Manual`: still best fetched manually through a browser or official portal.

### 16.1 P0 sources acquired in this batch

- `regulatory_rbi/rbi_floating_rate_emi_reset_2023_clean_extract.txt`
  - Status: Acquired - clean extract
  - Source URL: `https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12529`
  - Use for: floating EMI reset, tenor extension, EMI increase, quarterly statement and communication complaints.

- `regulatory_rbi/rbi_interest_rate_on_advances_directions_2016.txt`
  - Status: Acquired - snapshot
  - Source URL: `https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=10295`
  - Use for: interest rate reset, MCLR, external benchmark, loan pricing foundation.

- `regulatory_rbi/rbi_kfs_loans_advances_2024_clean_extract.txt`
  - Status: Acquired - clean extract
  - Source URL: `https://rbi.org.in/Scripts/NotificationUser.aspx?Id=12663&Mode=0`
  - Use for: KFS, APR, undisclosed fees, third-party charges, retail/MSME term loan transparency.

- `regulatory_rbi/rbi_fair_lending_penal_charges_loan_accounts_2023.txt`
  - Status: Already acquired earlier
  - Use for: penal charges vs penal interest.

- `regulatory_rbi/rbi_fraud_risk_management_commercial_banks_2024.txt`
  - Status: Acquired - snapshot
  - Source URL: `https://www.rbi.org.in/scriptS/BS_ViewMasDirections.aspx?id=12702`
  - Use for: fraud-risk governance, early warning signals, fraud monitoring and bank-side fraud workflow context.

- `regulatory_rbi/rbi_beaware_fraud_booklet_2022.pdf`
  - Status: Acquired - PDF
  - Source URL: `https://rbidocs.rbi.org.in/rdocs/content/pdfs/BEAWARE07032022.pdf`
  - Use for: fraud typologies, phishing, fake KYC, OTP/PIN, digital scam awareness.

- `regulatory_rbi/rbi_fame_financial_awareness_fraud_upi_customer_liability.txt`
  - Status: Already acquired as text snapshot
  - Note: Direct PDF download was blocked from this environment.
  - Use for: fraud-awareness and UPI/customer-liability user education.

- `regulatory_rbi/rbi_bbps_master_direction_2024_clean_extract.txt`
  - Status: Acquired - clean extract
  - Source URL: `https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12616&Mode=0`
  - Use for: BBPS bill-payment disputes, BBPS reference number, NBBL/COU/BOU responsibilities.

- `regulatory_rbi/rbi_online_dispute_resolution_digital_payments_2020_clean_extract.txt`
  - Status: Already acquired as clean extract
  - Source URL: `https://www.rbi.org.in/commonman/English/Scripts/Notification.aspx?Id=3194`
  - Use for: ODR, in-app dispute lodging, unique reference number and dispute tracking.

- `npci_upi/npci_upi_help_guidelines_reason_codes_p0_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: UPI Help reason codes such as U008, U021, U022, U023, U010, U005.

- `npci_upi/npci_upi_help_complaint_reference_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: UPI Help complaint reference number and complaint tracker flow.

- `npci_upi/npci_upi_dispute_redressal_mechanism_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: UPI dispute redressal flow and confirmation that customers use in-app UPI Help instead of a separate PDF form.

- `npci_upi/npci_rupay_chargeback_page_snapshot.txt`
  - Status: Acquired - snapshot
  - Source URL: `https://www.npci.org.in/what-we-do/rupay/chargeback`
  - Use for: RuPay chargeback page and chargeback statistics/context.

- `npci_upi/npci_netc_chargeback_reason_codes_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: chargeback reason-code style evidence, though NETC is not core MVP.

- `regulatory_rbi/rbi_customer_service_banks_master_circular_deposit_accounts.txt`
  - Status: Already acquired
  - Use for: customer-service and retail-banking anchor source.

- `regulatory_rbi/rbi_customer_rights_and_ombudsman_faq_context.txt`
  - Status: Already acquired
  - Use for: Charter of Customer Rights context.

- `regulatory_rbi/rbi_deceased_customer_claims_notification_2025_p0_fetch.txt`
  - Status: Acquired - snapshot
  - Source URL: `https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=12901&Mode=0`
  - Use for: deceased depositor claims, nominee/legal heir settlement, safe custody and locker claim settlement.

- `regulatory_rbi/rbi_safe_deposit_locker_notification_2021.txt`
  - Status: Already acquired
  - Use for: safe deposit locker agreement, bank liability and duty of care.

- `regulatory_rbi/rbi_udgam_unclaimed_deposits_portal_notes.txt`
  - Status: Already acquired as notes
  - Note: UDGAM PDF download was blocked from this environment.

- `regulatory_rbi/dicgc_information_booklet_2025.pdf`
  - Status: Acquired - PDF
  - Source URL: `https://www.dicgc.org.in/sites/default/files/2025-02/dicgc-information-booklet.pdf`
  - Use for: deposit insurance, bank liquidation/AID, Rs. 5 lakh insurance coverage.

### 16.2 P0 insurance sources already covered by snapshots, but original PDFs still recommended

- `insurance_irdai/irdai_health_insurance_master_circular_2024_document_page.txt`
  - Status: Acquired - document page snapshot
  - Manual still recommended: download the English PDF and annexure from IRDAI.

- `insurance_irdai/irdai_policyholders_interests_claims_grievance_2024.txt`
  - Status: Acquired - snapshot
  - Manual still recommended: download final English PDF of the Master Circular on Protection of Policyholders' Interests 2024.

### 16.3 P0 still manual or partially manual

1. RBI Floating Rate EMI FAQ PDF
   - Direct URL attempted: `https://www.rbi.org.in/commonman/Upload/English/FAQs/PDFs/FAQRFIR10012025.pdf`
   - Result: direct download blocked with small RBI error file.
   - Manual action: open in browser and save PDF.

2. RBI FAME 2024 PDF
   - Direct URL attempted: `https://www.rbi.org.in/commonman/images/FAME202426022024.pdf`
   - Result: direct download blocked with small RBI error file.
   - Current substitute: `rbi_fame_financial_awareness_fraud_upi_customer_liability.txt`

3. RBI UDGAM FAQ PDF
   - Direct URL attempted: `https://www.rbi.org.in/commonman/Upload/English/FAQs/PDFs/FAQonUDGAMPortal.pdf`
   - Result: direct download blocked.
   - Current substitute: `rbi_udgam_unclaimed_deposits_portal_notes.txt`

4. RBI DEA Fund FAQ PDF
   - Direct URL attempted: `https://www.rbi.org.in/commonman/Upload/English/FAQs/PDFs/FAQonDEAFundScheme2014_05032024.pdf`
   - Result: direct download blocked.
   - Current substitute: UDGAM/DEA notes plus RBI snapshots.

5. NPCI UDIR technical circular
   - Search result found old `Circular-98-UDIR-Enhancing-Complaint-handling-and-resolution.pdf`, but the public URL returned 404.
   - Current substitute: UPI Help guideline, UPI Help Assistant pilot, UPI chargeback snapshots.
   - Manual action: search NPCI circulars manually for `UDIR`, `OC 145A`, `OC 165`, `OC 184`, `OC 184B`.

6. NPCI RuPay detailed chargeback rules
   - Public RuPay chargeback page acquired.
   - Detailed rules may be operational/member-only or scattered across circulars.
   - Manual action: search `site:npci.org.in RuPay chargeback circular PDF reason code`.

7. IRDAI Health Insurance Master Circular 2024 English PDF and annexure
   - Document page acquired.
   - Manual action: open `https://irdai.gov.in/en/document-detail?documentId=4942918` and download English PDF + annexure.

8. IRDAI Protection of Policyholders' Interests 2024 English PDF
   - Snapshot acquired.
   - Manual action: open IRDAI document detail and download final English PDF.

### 16.4 P0 next step

Before P1 downloads, review whether the current substitutes are acceptable for implementation. For RAG MVP, clean extracts are often better than raw PDFs. Original PDFs are useful later for page-level citations and proof in README.


## 17. P1 Core Regulatory Acquisition Status

This section records the first P1 batch. It intentionally excludes the large bank-specific policy crawl, which should be done only after deciding which banks will be enabled in the demo.

### 17.1 P1 core sources acquired

- `regulatory_rbi/rbi_credit_information_companies_master_direction_2025_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Credit Information Company and Credit Institution complaint handling, correction/update workflows.

- `regulatory_rbi/rbi_cic_compensation_framework_notification_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Rs. 100/day compensation for delayed credit information correction beyond 30 calendar days.

- `regulatory_rbi/rbi_interest_rate_on_advances_directions_2016_p1_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: MCLR, external benchmark, interest-rate reset and loan pricing context.

- `regulatory_rbi/rbi_fraud_risk_management_commercial_banks_p1_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: fraud-risk management directions, early warning signals, red-flagged accounts, bank-side fraud reporting.

- `regulatory_rbi/rbi_fraud_risk_management_notification_p1.txt`
  - Status: Acquired - snapshot
  - Use for: notification version of fraud-risk management directions.

- `regulatory_rbi/rbi_fraudulent_electronic_transactions_rcb_context_p1.txt`
  - Status: Acquired - snapshot
  - Use for: fraudulent electronic banking transaction handling in cooperative bank context; useful supporting material.

- `npci_upi/npci_rupay_chargeback_page_p1_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: RuPay chargeback page and chargeback statistics/context.

- `npci_upi/npci_netc_chargeback_reason_codes_p1_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: chargeback reason-code style evidence; not core UPI but useful for dispute taxonomy.

- `npci_upi/npci_upi_chargeback_archive_p1_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: UPI chargeback archive context and statistics.

- `regulatory_rbi/rbi_ombudsman_annual_report_2024_25_p1_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: complaint category prioritization and product analytics.

- `regulatory_rbi/rbi_ombudsman_annual_report_2023_24_p1_snapshot.txt`
  - Status: Acquired - snapshot
  - Use for: complaint trend comparison and evaluation category design.

### 17.2 P1 still pending or manual

- Bank-specific customer compensation policies for HDFC, ICICI, Axis, SBI, Kotak, IDFC FIRST.
  - Some text snapshots are already available, but official PDFs should be manually downloaded for README proof/page-level citations.

- Public-sector bank grievance/deposit/cheque policies:
  - Bank of Baroda
  - Canara Bank
  - Punjab National Bank
  - Union Bank of India

- Additional private/foreign bank policies:
  - Federal Bank
  - AU Small Finance Bank
  - HSBC India
  - Standard Chartered India full card MITC

Recommendation:

- Do not crawl these bank-specific policies blindly. First choose 5-7 demo banks, then collect their complete policy sets:
  - grievance redressal policy
  - customer compensation policy
  - deposit policy
  - cheque collection policy
  - debit card MITC
  - credit card MITC
  - deceased depositor policy


## 18. P1 Bank-Specific Policy Pack - First Six Demo Banks

This section records the first bank-specific P1 acquisition batch for HDFC, ICICI, Axis, SBI, Kotak and IDFC FIRST. These sources are useful for building institution-specific answers after metadata filters are working.

Implementation rule:

- Use RBI documents first for general rules.
- Use bank-specific files only when the user names that bank or selects it in the UI.
- Never present one bank's policy as a universal banking rule.

### 18.1 HDFC Bank

- `bank_documents/hdfc_citizens_charter_policy_index_p1.txt`
  - Status: Acquired - snapshot
  - Use for: HDFC Citizen's Charter, cheque collection, compensation and deceased account policy links/context.

- `bank_documents/hdfc_deceased_depositors_nomination_policy_p1.txt`
  - Status: Acquired - snapshot
  - Use for: HDFC deceased depositor and nomination rules.

Already available HDFC files:

- `bank_documents/hdfc_credit_card_mitc_english.pdf`
- `bank_documents/hdfc_credit_card_policy.pdf`
- `bank_documents/hdfc_purchase_card_mitc_compensation_context.txt`

Manual still useful:

- HDFC Customer Compensation Policy June 2025 PDF
- HDFC Cheque Collection Policy PDF
- HDFC Deposit Policy PDF if available

### 18.2 ICICI Bank

- `bank_documents/icici_savings_account_terms_deposit_cheque_nomination_p1.txt`
  - Status: Acquired - snapshot
  - Use for: savings account terms, cheque book, collection facility, nomination/deceased account context.

Already available ICICI files:

- `bank_documents/icici_credit_card_mitc.pdf`
- `bank_documents/icici_credit_card_mitc_web_terms_dispute_context.txt`
- `bank_documents/icici_customer_grievance_redressal_policy.pdf`
- `bank_documents/icici_feedback_complaint_page.txt`

Manual still useful:

- From `https://www.icicibank.com/customer-service-policies`, download:
  - Grievance Redressal Policy
  - Cheque Collection Policy
  - Policy on Collection of Dues and Repossession of Security
  - Customer Rights Policy
  - Deposit Policy
  - Customer Relations Policy
  - Compensation Policy
  - Deceased Depositors Policy

### 18.3 Axis Bank

- `bank_documents/axis_cheque_collection_policy_2025_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Axis cheque collection timelines and delayed collection compensation.

- `bank_documents/axis_deceased_depositor_claim_policy_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Axis deceased depositor claim settlement, nominee/survivor/legal heir process.

- `bank_documents/axis_code_of_commitment_cheque_deceased_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Axis cheque collection, compensation, deceased account and grievance commitments.

Already available Axis files:

- `bank_documents/axis_grievance_redressal_policy_2026.pdf`
- `bank_documents/axis_credit_card_mitc.pdf`
- `bank_documents/axis_debit_card_mitc_grievance_compensation.txt`
- `bank_documents/axis_code_of_commitment.pdf`

Manual still useful:

- Axis Customer Compensation Policy PDF.
- Axis Comprehensive Deposit Policy PDF.

### 18.4 State Bank of India

- `bank_documents/sbi_customer_rights_grievance_compensation_policy_2023_p1.txt`
  - Status: Acquired - snapshot
  - Use for: SBI customer rights, grievance redressal, compensation, cheque and digital transaction failures.

- `bank_documents/sbi_policy_on_depositors_rights_2025_p1.txt`
  - Status: Acquired - snapshot
  - Use for: SBI depositor rights, deposit account operations, grievance and compensation context.

- `bank_documents/sbi_cheque_collection_policy_2017_p1.txt`
  - Status: Acquired - snapshot
  - Use for: SBI cheque collection and delayed collection compensation.

- `bank_documents/sbi_multi_city_cheque_policy_p1.txt`
  - Status: Acquired - snapshot
  - Use for: SBI multi-city cheque issuance/collection/dishonour.

Already available SBI Card files:

- `bank_documents/sbi_card_customer_grievance_policy.pdf`
- `bank_documents/sbi_card_mitc_english.pdf`

Manual still useful:

- Latest SBI cheque collection policy if newer than 2017.
- SBI deceased depositor claim policy/forms.

### 18.5 Kotak Mahindra Bank

- `bank_documents/kotak_deceased_claim_page_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Kotak deceased claim process page.

Already available Kotak files:

- `bank_documents/kotak_grievance_redressal_policy.txt`
- `bank_documents/kotak_811_dream_different_kfs_grievance.pdf`
- `bank_documents/kotak_white_reserve_kfs_grievance.pdf`

Manual still useful:

- From Kotak Banking Policies page, download:
  - Customer Rights Policy
  - Policy on Collection of Dues and Repossession of Security
  - Policy for Cheque Collection
  - Customer Compensation Policy
  - Deposit Policy
  - Credit Card Board Policy
  - Code of Conduct for Direct Selling Agents

### 18.6 IDFC FIRST Bank

- `bank_documents/idfc_cheque_collection_policy_2025_p1.txt`
  - Status: Acquired - snapshot
  - Use for: IDFC FIRST cheque collection, delayed collection, lost instruments and compensation.

- `bank_documents/idfc_grievance_redressal_policy_2024_p1.txt`
  - Status: Acquired - snapshot
  - Use for: IDFC FIRST grievance policy, ATM failure, unauthorized electronic transaction shadow reversal and 90-day resolution.

- `bank_documents/idfc_deceased_depositors_claim_process_forms_p1.txt`
  - Status: Acquired - snapshot
  - Use for: IDFC FIRST deceased depositor claim process and forms.

Already available IDFC files:

- `bank_documents/idfc_escalation_matrix_tat.pdf`
- `bank_documents/idfc_credit_card_mitc.pdf`
- `bank_documents/idfc_general_terms_grievance_context.txt`

Manual still useful:

- IDFC FIRST Customer Compensation Policy PDF if separately published.
- IDFC FIRST Deposit Policy PDF if separately published.

### 18.7 Next bank-specific batch

If continuing bank-specific collection, recommended order:

1. Bank of Baroda
2. Canara Bank
3. Punjab National Bank
4. Union Bank of India
5. Federal Bank
6. AU Small Finance Bank
7. HSBC India
8. Standard Chartered India full card MITC set

For each bank, collect the same standard policy pack:

- grievance redressal policy
- customer compensation policy
- deposit policy
- cheque collection policy
- deceased depositor policy/forms
- debit card MITC
- credit card MITC
- collection/recovery policy


## 19. P1 Bank-Specific Policy Pack - Second Batch

This section covers additional banks beyond the first six demo banks. These sources are useful for broader bank coverage, but should only be enabled in the app once metadata filtering by institution is implemented.

### 19.1 Bank of Baroda

- `bank_documents/bob_code_of_commitment_customers_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Bank of Baroda customer commitments, cheque collection, compensation, deceased account claim and grievance context.

- `bank_documents/bob_grievance_redressal_hindi_snapshot_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Bank of Baroda grievance process and SPGRS tracker ID context.

- `bank_documents/bob_death_claim_settlement_process_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Bank of Baroda deceased depositor claim process and 15-calendar-day settlement reference.

Manual still useful:

- Bank of Baroda customer compensation policy PDF.
- Bank of Baroda cheque collection policy PDF.
- Bank of Baroda deposit policy PDF.

### 19.2 Canara Bank

- `bank_documents/canara_download_center_policy_index_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Canara download center and forms/policy discovery.

- `bank_documents/canara_grievance_redressal_policy_2025_26_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Canara grievance redressal policy, cheque acknowledgement, customer service committee, failed transaction references.

- `bank_documents/canara_deposit_policy_2025_26_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Canara deposit policy, cheque books, interest on deceased depositor term deposits.

- `bank_documents/canara_death_claim_settlement_policy_2024_25_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Canara death claim settlement, portal workflow, documents and branch verification.

Manual still useful:

- Canara cheque collection policy PDF.
- Canara customer compensation policy PDF.
- Canara debit/credit card MITC documents.

### 19.3 Punjab National Bank

- `bank_documents/pnb_deposit_policy_and_grievance_notes_p1.txt`
  - Status: Acquired - clean notes
  - Use for: PNB deposit policy page, grievance redressal route, complaint timelines and forms discovery.

Manual still useful:

- PNB grievance redressal policy PDF.
- PNB customer compensation policy PDF.
- PNB cheque collection policy PDF.
- PNB customer rights policy PDF.
- PNB deceased account claim forms.

### 19.4 Union Bank of India

- `bank_documents/union_bank_death_claim_and_grievance_notes_p1.txt`
  - Status: Acquired - clean notes
  - Use for: Union Bank death claim portal, 2026-27 death claim policy link, contact/grievance/fraud helpline context.

Manual still useful:

- Union Bank Policy on Settlement of Death Claim 2026-2027 PDF.
- Union Bank customer compensation policy PDF.
- Union Bank deposit policy PDF.
- Union Bank cheque collection policy PDF.
- Union Bank grievance redressal policy PDF.

### 19.5 Federal Bank

- `bank_documents/federal_policy_on_customer_service_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Federal Bank customer service, grievance mechanism, cheque collection and service commitments.

- `bank_documents/federal_customer_grievance_redressal_policy_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Federal Bank grievance redressal policy.

- `bank_documents/federal_policy_on_bank_deposits_2025_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Federal Bank deposit policy, account operations, depositor rights and complaint route.

- `bank_documents/federal_customer_compensation_policy_p1.txt`
  - Status: Acquired - snapshot
  - Use for: Federal Bank customer compensation policy, cheque delay compensation and service deficiency.

Manual still useful:

- Federal Bank deceased depositor policy if separately published.
- Federal Bank debit/credit card MITC.

### 19.6 HSBC India

- `bank_documents/hsbc_regulatory_disclosures_policy_index_p1.txt`
  - Status: Acquired - snapshot
  - Use for: HSBC policy index with cheque collection, deceased claims, compensation and deposit policy links.

- `bank_documents/hsbc_branch_notices_policy_index_p1.txt`
  - Status: Acquired - snapshot
  - Use for: HSBC branch notices and policy document discovery.

- `bank_documents/hsbc_forms_credit_card_dispute_mitc_p1.txt`
  - Status: Acquired - snapshot
  - Use for: HSBC forms, credit card dispute form, credit card MITC discovery, unclaimed deposits claim form.

- `bank_documents/hsbc_credit_card_faq_dispute_p1.txt`
  - Status: Acquired - snapshot
  - Use for: HSBC card dispute process, chargeback contact, credit card consent and service guide references.

Manual still useful:

- HSBC compensation policy PDF.
- HSBC cheque collection policy PDF.
- HSBC deceased depositor / safe locker policy PDF.
- HSBC credit card MITC PDFs for selected cards.

### 19.7 Standard Chartered India

- `bank_documents/standard_chartered_policy_links_notes_p1.txt`
  - Status: Acquired - clean notes
  - Use for: Standard Chartered compensation policy, cheque collection policy and card MITC link discovery.

Already available:

- `bank_documents/standard_chartered_grievance_redressal_policy.pdf`

Manual still useful:

- Standard Chartered compensation policy PDF:
  - `https://av.sc.com/in/content/docs/in-compensation-policy.pdf`
- Standard Chartered cheque collection policy PDF.
- Standard Chartered credit card MITC PDFs for selected cards.

### 19.8 AU Small Finance Bank

- `bank_documents/au_small_finance_bank_rbi_awareness_locator_p1_low_authority.txt`
  - Status: Acquired - low authority / locator snapshot
  - Use for: only basic AU contact/RBI awareness context.
  - Warning: This is not a strong policy source.

Manual still required:

- AU Small Finance Bank grievance redressal policy.
- AU customer compensation policy.
- AU deposit policy.
- AU cheque collection policy.
- AU deceased claim policy.
- AU debit/credit card terms if applicable.

### 19.9 Recommendation after second bank batch

For implementation, enable bank-specific answers only for banks with reasonably complete source packs:

- HDFC
- ICICI
- Axis
- SBI
- Kotak
- IDFC FIRST
- Federal Bank
- Canara Bank
- Bank of Baroda

Keep `PNB`, `Union Bank`, `HSBC`, `Standard Chartered`, and `AU Small Finance Bank` as partial coverage until their full PDFs are manually downloaded.

### 19.10 Supplemental files saved after follow-up search

- `bank_documents/bob_code_of_commitment_customers_p1_refreshed.txt`
  - Refreshed Bank of Baroda customer commitment snapshot.

- `bank_documents/bob_deposit_faq_other_services_p1.txt`
  - Bank of Baroda deposit/other services FAQ snapshot.

- `bank_documents/bob_death_claim_settlement_process_p1_refreshed.txt`
  - Refreshed Bank of Baroda deceased claim settlement page snapshot.

- `bank_documents/union_bank_death_claim_policy_2026_27_p1.txt`
  - Union Bank death claim policy 2026-27 snapshot.

- `bank_documents/hsbc_regulatory_disclosures_policy_index_p1_refreshed.txt`
  - Refreshed HSBC regulatory disclosures index.

- `bank_documents/hsbc_branch_notices_policy_index_p1_refreshed.txt`
  - Refreshed HSBC branch notices/policy index.

- `bank_documents/hsbc_account_terms_charges_deceased_context_p1.txt`
  - HSBC account terms, service charges and deceased depositor context.

- `bank_documents/hsbc_forms_credit_card_dispute_unclaimed_deposits_p1.txt`
  - HSBC forms page with credit card dispute, MITC and unclaimed deposit claim references.
