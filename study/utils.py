from django.http import JsonResponse
from study.models import Teacher
import json


def get_body(request):
    """
    :param request: Django http request instance
    :return: data from x-www-form-urlencoded or json body
    """
    try:
        return json.loads(request.body)
    except:
        return request.POST


def verify_data(data: dict, contains: list) -> str or None:
    """
    :param data: body dict
    :param contains: contents must be contained in body
    :return: None if no problem, else return name of required content
    """
    for c in contains:
        if c not in data:
            return c
    return None


def get_response(code: int, data: dict or list = None, msg: str = None) -> JsonResponse:
    """
    :param code: status code for response
    :param data: body for response or data included in message
    :param msg: message for error
    :return:
    """
    if code == 200:  # Success
        response = {
            'status_code': code,
            'message': 'Success'
        }
        if data:
            response['data'] = data
        return JsonResponse(response)
    elif code == 400:  # Unknown user error
        return JsonResponse({
            'status_code': code,
            'message': msg,
        })
    elif code == 405:  # Method is not allowed
        return JsonResponse({
            'status_code': code,
            'message': msg if msg else 'Method %s is not allowed. (%s)' % (data[0], ', '.join(data[1:]))
        })
    elif code == 500:  # Unknown server error
        return JsonResponse({
            'status_code': code,
            'message': msg if msg else 'Internal server error.'
        })


def teacher_to_json(teacher: Teacher) -> dict:
    """
    :param teacher: Teacher instance of model
    :return: dict form json data
    """
    return {
        'username': teacher.username,
        'fullname': teacher.fullname,
        'email': teacher.email,
        'birthday': teacher.birthday
    }