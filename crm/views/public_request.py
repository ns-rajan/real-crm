from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from tenants.models import Agency
from crm.forms.public_request_form import PublicRequestForm


@csrf_exempt
def public_request(request, agency_id: int):
    """
    Public-facing endpoint to create a tenant-scoped Request.

    - URL carries the tenant identifier (agency_id).
    - The form is scoped to that agency (for resources).
    - The created Request instance is tagged with the agency.
    """
    agency = get_object_or_404(Agency, pk=agency_id)

    if request.method == "GET":
        form = PublicRequestForm(agency=agency)
        return render(
            request,
            "public_request.html",
            {"form": form, "agency": agency},
        )

    if request.method == "POST":
        form = PublicRequestForm(request.POST, agency=agency)
        if not form.is_valid():
            # For non-AJAX usage, you might want to re-render the template.
            # Here we keep JSON errors for easy integration.
            return JsonResponse({"errors": form.errors}, status=400)

        # Create the Request, forcing the tenant agency from the URL.
        instance = form.save(commit=False)
        instance.agency = agency
        instance.save()
        form.save_m2m()

        # Simple confirmation response for the public form.
        return HttpResponse("Thank you! Your request has been submitted.")

    return HttpResponse(status=405)

