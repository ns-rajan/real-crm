import os
import json
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

def parse_identity_document(file_bytes: bytes, mime_type: str) -> dict:
    """
    Takes raw file bytes and a mime_type (e.g., 'image/jpeg', 'application/pdf'),
    sends it to the Vision LLM, and returns a strictly formatted dictionary.
    """
    try:
        # Initialize client. Automatically picks up GEMINI_API_KEY from environment.
        client = genai.Client()
        
        # Use a fast multimodal model
        model_id = 'gemini-2.5-flash' 
        
        # The prompt enforcing our exact schema requirements
        prompt = """
        You are an expert KYC document parser. Analyze the attached document. 
        Extract the requested data and return ONLY a valid JSON object matching this exact schema. 
        Do not include any conversational text or markdown formatting.
        
        Schema:
        {
          "document_type": "passport | national_id | nif | bank_statement | lease_statement | other",
          "confidence_score": 0.0 to 1.0,
          "extracted_data": {
            "first_name": "string or null",
            "last_name": "string or null",
            "id_number": "string or null",
            "expiry_date": "YYYY-MM-DD or null",
            "dob": "YYYY-MM-DD or null",
            "gender": "M | F | O or null",
            "address": "string or null",
            "city": "string or null",
            "county": "string or null",
            "state": "string or null",
            "country": "string or null"
          }
        }
        """
        
        # Configure the request to force JSON output
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1, # Keep it deterministic and strict
        )
        
        # Pass the bytes directly to the model
        response = client.models.generate_content(
            model=model_id,
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                prompt
            ],
            config=config
        )
        
        # Parse the guaranteed JSON string into a Python dictionary
        parsed_data = json.loads(response.text)
        return parsed_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from LLM: {e}")
        return _fallback_error_response("json_parse_error")
    except Exception as e:
        logger.error(f"LLM Parsing failed: {e}")
        return _fallback_error_response("llm_connection_error")

def _fallback_error_response(error_type: str) -> dict:
    """Returns a safe, empty dictionary structure so the CRM doesn't crash."""
    return {
        "document_type": "other",
        "confidence_score": 0.0,
        "error": error_type,
        "extracted_data": {
            "first_name": None,
            "last_name": None,
            "id_number": None,
            "expiry_date": None,
            "dob": None,
            "gender": None,
            "address": None,
            "city": None,
            "county": None,
            "state": None,
            "country": None
        }
    }