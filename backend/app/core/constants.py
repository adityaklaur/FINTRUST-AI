"""Application-wide constants.

Kept dependency-free so any module can import it without side effects.
"""

APP_NAME = "FinTrust AI"
APP_VERSION = "0.1.0"

# ChromaDB collection that holds every ingested chunk for the MVP.
DEFAULT_COLLECTION = "fintrust_v1"

# The mandatory safety line appended to every generated answer.
DISCLAIMER = (
    "⚠️ This is not legal, financial, or regulatory advice. "
    "Information is sourced from public documents and may not reflect the latest "
    "updates. Always verify with the official source or a qualified professional."
)
