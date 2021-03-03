from django.http import JsonResponse
from study.models import Teacher, Student, Content, Category, Curriculum
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


def logged_in_student(request) -> Student or None:
    student_id = request.session.get('student')
    if student_id:
        try:
            student = Student.objects.get(id=student_id)
            return student
        except:
            return None
    return None


def logged_in_teacher(request) -> Teacher or None:
    teacher_id = request.session.get('teacher')
    if teacher_id:
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            return teacher
        except:
            return None
    return None


def verify_data(data: dict, contains: list) -> JsonResponse or None:
    """
    :param data: body dict
    :param contains: contents must be contained in body
    :return: None if no problem, else return name of required content
    """
    for c in contains:
        if c not in data:
            return get_response(400, msg='(%s) is required in body.' % (', '.join(contains)))
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
    elif code == 401:  # Unknown user error
        return JsonResponse({
            'status_code': code,
            'message': 'User is unauthorized.',
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


def to_json(object: Teacher or Student or Content or Category or Curriculum) -> dict:
    """
    :param object: instance of models
    :return: dict form json data
    """
    if isinstance(object, Teacher):
        return {
            'username': object.username,
            'fullname': object.fullname,
            'email': object.email,
            'birthday': object.birthday
        }
    elif isinstance(object, Student):
        return {
        }
    elif isinstance(object, Content):
        return {
            'id': object.id,
            'title': object.title,
            'level': object.level,
            'teacher': {
                'id': object.teacher_id,
                'fullname': object.teacher.fullname
            }
        }
    elif isinstance(object, Category):
        return {
            'id': object.id,
            'english': object.english
        }
    elif isinstance(object, Curriculum):
        return {

        }


def get_detail_content(content: Content) -> dict:
    return {
        'id': content.id,
        'category': content.category_id,
        'type': content.type,
        'title': content.title,
        'level': content.level,
        'teacher': {
            'id': content.teacher_id,
            'fullname': content.teacher.fullname
        },
        'content': content.content
    }