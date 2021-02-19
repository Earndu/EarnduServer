import json
from study.models import Teacher
import traceback
from django.db.utils import IntegrityError
from study.utils import get_response, verify_data, teacher_to_json, get_body


def teacher_many(request):
    if request.method == 'POST':  # Insert new teacher data
        body = get_body(request)
        required = ['username', 'password', 'fullname', 'email', 'birthday']
        verify = verify_data(body, required)
        if verify:
            return get_response(400, msg='(%s) is required in body.' % (', '.join(required)))

        try:
            Teacher.objects.create(
                username=body['username'],
                password=body['password'],
                fullname=body['fullname'],
                email=body['email'],
                birthday=body['birthday']
            )

            return get_response(200)
        except IntegrityError:
            return get_response(400, msg='Username already exists. (%s)' %body['username'])
        except:
            return get_response(500, msg=traceback.format_exc())
    else:
        return get_response(405, [request.method, 'POST'])


def teacher_one(request, teacher_id):
    if request.method == 'GET':
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            return get_response(200, teacher_to_json(teacher))
        except Teacher.DoesNotExist:
            return get_response(400, msg='Teacher id does not exist. (%s)' % teacher_id)
        except:
            return get_response(500, msg=traceback.format_exc())
    else:
        return get_response(405, [request.method, 'GET'])


def teacher_login(request):
    if request.method == 'POST':
        teacher_id = request.session.get('teacher')
        if teacher_id:
            teacher = Teacher.objects.get(id=teacher_id)
            return get_response(400, msg='User has already logged in. (%s)' % teacher.username)

        body = get_body(request)
        required = ['username', 'password']
        verify = verify_data(body, required)
        if verify:
            return get_response(400, msg='(%s) is required in body.' % (', '.join(required)))

        try:
            teacher = Teacher.objects.get(username=body['username'], password=body['password'])
            request.session['teacher'] = teacher.id
            return get_response(200)
        except Teacher.DoesNotExist:
            return get_response(400, msg='Username or password does not match.')
        except:
            return get_response(500, msg=traceback.format_exc())
    else:
        return get_response(405, [request.method, 'POST'])
