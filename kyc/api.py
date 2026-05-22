import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .services import process_kyc_document

@csrf_exempt  # Disabled strictly for frictionless PoC testing
@require_POST
def upload_kyc_endpoint(request):
    """
    Expects a multipart/form-data request with a 'kyc_file' attached.
    """
    if 'kyc_file' not in request.FILES:
        return JsonResponse({"error": "No 'kyc_file' provided in the request."}, status=400)

    uploaded_file = request.FILES['kyc_file']

    # Hand the file over to the service layer
    result = process_kyc_document(uploaded_file)

    if result.get("error") and not result.get("extracted_data"):
        return JsonResponse(result, status=500)

    return JsonResponse(result, status=200)