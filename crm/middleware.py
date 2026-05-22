import time
import logging
from django.db import connection

logger = logging.getLogger(__name__)

class NeonColdStartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        was_connected = connection.connection is not None
        
        response = self.get_response(request)
        
        total_duration = time.time() - start_time
        
        if total_duration > 2.0:
            query_time = sum(float(q.get('time', 0)) for q in connection.queries)
            logger.warning(
                f"Slow Request ({request.path}): {total_duration:.2f}s total. "
                f"DB Exec Time: {query_time:.2f}s for {len(connection.queries)} queries. "
                f"Initial DB Connection Active: {was_connected}"
            )
            
        return response