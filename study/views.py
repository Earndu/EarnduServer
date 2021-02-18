import json
from study.models import Teacher
import traceback
from django.db.utils import IntegrityError
from study.utils import get_response, verify_data, teacher_to_json


def teacher_many(request):
    if request.method == 'POST':  # Insert new teacher data
        # Load data from x-www-form-urlencoded or json body
        body = request.POST
        try:
            body = json.loads(request.body)
        except:
            pass

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
        except IntegrityError:
            return get_response(400, msg='Username already exists. (%s)' %body['username'])
        except:
            return get_response(500, msg=traceback.format_exc())

        return get_response(200)
    else:
        return get_response(405, [request.method, 'POST'])


def teacher_one(request, teacher_id):
    if request.method == 'GET':
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return get_response(400, msg='Teacher id does not exist. (%s)' % teacher_id)
        except:
            return get_response(500, msg=traceback.format_exc())

        return get_response(200, teacher_to_json(teacher))
    else:
        return get_response(405, [request.method, 'GET'])
