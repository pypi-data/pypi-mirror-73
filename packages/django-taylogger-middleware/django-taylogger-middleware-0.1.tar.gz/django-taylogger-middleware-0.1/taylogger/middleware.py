from .utils import TayLoggerAPIConsumer
from django.conf import settings


class ErrorLoggerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if hasattr(settings, "TAYLOGGER_API_KEY"):

            api_key = settings.TAYLOGGER_API_KEY
            taylogger_consumer = TayLoggerAPIConsumer(api_key)

            if hasattr(settings, "EXCEPTION_GROUP_ID"):
                group_id = settings.EXCEPTION_GROUP_ID
                taylogger_consumer.create_log({"group": group_id, "message": str(exception)})
            else:
                print('\x1b[3;37;41m' + "WARNING!, You have not added your Taylogger Group Id to settings" + '\x1b[0m')

        else:
            print('\x1b[3;37;41m' + "WARNING!, You have not added your Taylogger API key to settings" + '\x1b[0m')
