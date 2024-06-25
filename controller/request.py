import requests


class RequestCommands:

    @classmethod
    def get_previous_url(cls, request):
        if 'HTTP_REFERER' in request.META:
            return request.META['HTTP_REFERER']
        else:
            False
        
    
class RequestWhatsapp:

    @classmethod
    def notification_wpp(cls, number: str, message: str):
        url = 'http://192.168.1.10:8004/notification/wpp'
        data = {
            "number": number,
            "message": message
        }
        requests.post(url, json=data)
