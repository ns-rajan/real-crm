# crm/views/kyc_views.py
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from crm.services import onboard_contact_via_kyc

# TODO: Remove @csrf_exempt and implement proper CSRF token handling via frontend JS headers
@staff_member_required
@csrf_exempt
def auto_create_contact_view(request):
    if request.method == 'POST' and request.FILES.get('document'):
        file = request.FILES['document']
        
        # 1. File Validation: Size (Max 5MB)
        if file.size > 5 * 1024 * 1024:
            return JsonResponse({"error": "File size exceeds 5MB limit. Please upload a smaller file."}, status=400)
            
        # 2. File Validation: Extension
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.pdf']:
            return JsonResponse({"error": f"Unsupported file extension '{ext}'. Allowed types are JPG, PNG, and PDF."}, status=400)

        mode = request.POST.get('mode', 'create')
        
        result = onboard_contact_via_kyc(file, request.user, mode)
        
        if result["success"]:
            status_code = 200 if result.get("action") == "updated" else 201
            return JsonResponse({"message": f"Contact {result.get('action')}!", "contact_id": result["contact_id"]}, status=status_code)
        else:
            if result.get("requires_update_confirmation"):
                # 409 Conflict triggers UI modal asking "Update Existing?"
                return JsonResponse({
                    "error": result.get("error"), 
                    "message": result.get("message"),
                    "contact_name": result.get("contact_name"),
                    "requires_update_confirmation": True, 
                    "contact_id": result.get("contact_id")
                }, status=409)

            return JsonResponse({"error": result.get("error") or result.get("message") or "Unknown error"}, status=400)
            
    return JsonResponse({"error": "Invalid request"}, status=400)