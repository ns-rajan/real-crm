import logging
from .parsers.llm_vision import parse_identity_document

logger = logging.getLogger(__name__)

def process_kyc_document(uploaded_file) -> dict:
    """
    The main orchestrator for KYC processing.
    Takes a Django UploadedFile, passes it to the AI parser,
    and applies business logic before returning the payload.
    """
    try:
        # 1. Extract bytes and mime type natively from Django's file object
        file_bytes = uploaded_file.read()
        mime_type = uploaded_file.content_type

        # 2. Call the AI Extraction Layer
        parsed_data = parse_identity_document(file_bytes, mime_type)

        # 3. (Future) The Validation Layer
        # Here is where you will eventually route the data to apps.kyc.validators
        # e.g., if parsed_data['document_type'] == 'nif_document':
        #           is_valid = validate_portuguese_nif(parsed_data['extracted_data']['tax_id_nif'])

        return parsed_data

    except Exception as e:
        logger.error(f"Error in KYC service orchestrator: {e}")
        return {
            "error": str(e),
            "document_category": "unknown",
            "extracted_data": None
        }