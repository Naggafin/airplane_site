import logging

from django.http import JsonResponse

logger = logging.getLogger(__name__)


def csp_report_view(request):
	if request.method == "POST":
		try:
			# Decode and log the CSP report
			report = request.body.decode("utf-8")
			logger.warning("CSP Violation Report: %s", report)
		except Exception as e:
			logger.error("Failed to process CSP report: %s", e)
	return JsonResponse({"status": "success"})
