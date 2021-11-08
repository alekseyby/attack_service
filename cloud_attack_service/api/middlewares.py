import time
from .models import APIStat


class StatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()

        response = self.get_response(request)
        if response.status_code == 200:
            end = time.time()

            time_diff = (end - start)
            APIStat.objects.create(response_time=time_diff)

        return response
