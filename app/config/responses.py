from rest_framework.response import Response
from rest_framework import status

class APIResponse(Response):
    def __init__(self, data=None, status=None, message=None, errors=None):
        response_data = {
            "status": "success" if status and status < 400 else "error",
            "message": message,
            "data": data,
            "errors": errors
        }
        super().__init__(response_data, status=status)