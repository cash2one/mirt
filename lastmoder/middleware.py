from . import get_last_time, datetime2rfc
from datetime import datetime


class SimpleCacheControlMiddleware(object):
    def process_response(self, request, response):
        response['Last-Modified'] = get_last_time()
        if request.method == 'GET':
            if len(request.GET) > 0:
                response['Last-Modified'] = datetime2rfc(datetime.now())
        if request.method == 'POST':
            if len(request.POST) > 0:
                response['Last-Modified'] = datetime2rfc(datetime.now())

        return response