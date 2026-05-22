import logging
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db import transaction
from kyc.services import process_kyc_document
from crm.models import Contact, Company, ContactDocument, Country
# from common.models import TheFile  # Uncomment if you use a central file manager

logger = logging.getLogger(__name__)

def onboard_contact_via_kyc(uploaded_file, user, mode="create"):
    """
    Takes a raw file upload, parses it via the KYC engine, 
    and automatically creates or updates a CRM Contact with linked document storage.
    """
    try:
        # 1. Send the file to our isolated AI engine (OUTSIDE database transaction)
        kyc_data = process_kyc_document(uploaded_file)

        if kyc_data.get("error"):
            return {"success": False, "error": kyc_data["error"]}

        extracted = kyc_data.get("extracted_data", {})
        
        id_num_raw = extracted.get("id_number")
        id_num = str(id_num_raw).strip() if id_num_raw else None

        # Start database transaction for write safety
        with transaction.atomic():
            existing_contact = None
            if id_num:
                existing_contact = Contact.objects.filter(id_number__iexact=id_num).first()
                
            # Duplicate check handling based on frontend 'mode'
            if existing_contact and mode != "update":
                return {
                    "success": False,
                    "error": "ID_EXISTS",
                    "message": f"Contact with ID number {id_num} already exists.",
                    "contact_name": existing_contact.full_name,
                    "requires_update_confirmation": True,
                    "contact_id": existing_contact.id
                }

            # 2. Map the JSON to your CRM Contact model
            comp, _ = Company.objects.get_or_create(full_name="Auto-Onboarded")

            # Handle Country resolving securely (it's a ForeignKey in BaseContact)
            country_str = extracted.get("country", "India")
            country_obj = Country.objects.filter(name__iexact=country_str).first() if country_str else None

            # Map gender to inherited sex choices ('M', 'F', 'O')
            gender = extracted.get("gender", "O")[:1].upper()
            if gender not in ['M', 'F', 'O']:
                gender = 'O'

            # Safely handle dates (Django DateFields crash on empty strings "")
            dob_raw = extracted.get("dob")
            dob = dob_raw if dob_raw else None
            
            expiry_raw = extracted.get("expiry_date")
            expiry = expiry_raw if expiry_raw else None

            if existing_contact and mode == "update":
                contact = existing_contact
                if extracted.get("first_name"): contact.first_name = extracted.get("first_name")
                if extracted.get("last_name"): contact.last_name = extracted.get("last_name")
                if gender != 'O': contact.sex = gender
                if expiry: contact.id_expiry = expiry
                if dob: contact.birth_date = dob
                contact.address = extracted.get("address") or contact.address
                contact.city_name = extracted.get("city") or contact.city_name
                contact.district = extracted.get("county") or contact.district
                contact.region = extracted.get("state") or contact.region
                if country_obj: contact.country = country_obj
                contact.kyc_verified = True
                contact.save()
                action = "updated"
            else:
                contact = Contact.objects.create(
                    company=comp,
                    created_by=user,  # Fixes the "empty" uploaded_by
                    first_name=extracted.get("first_name") or "Unknown",
                    last_name=extracted.get("last_name") or "",
                    sex=gender, 
                    id_number=id_num,
                    id_expiry=expiry,
                    birth_date=dob,
                    address=extracted.get("address") or "",
                    city_name=extracted.get("city") or "",
                    district=extracted.get("county") or "",
                    region=extracted.get("state") or "",
                    country=country_obj,
                    kyc_verified=True,
                    consent_timestamp=timezone.now()
                )
                action = "created"

            # 3. Save the physical file to the related Document table
            # Reset the file pointer to the beginning before saving
            uploaded_file.seek(0) 
            
            # Appends the document rather than over-writing to keep history
            ContactDocument.objects.create(
                contact=contact,
                document_type=kyc_data.get("document_type", "other"),
                file=uploaded_file
            )
            
            return {
                "success": True, 
                "contact_id": contact.id, 
                "parsed_data": kyc_data,
                "action": action
            }

    except Exception as e:
        # Crucial for debugging the 'not-null' or 'keyword argument' errors we saw
        logger.error(f"KYC Error: {e}")
        return {"success": False, "error": str(e)}