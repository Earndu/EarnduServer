import json
from study.models import Teacher, Student, Content, Category, Curriculum
import traceback
from django.db.utils import IntegrityError
from study.utils import get_response, verify_data, to_json, get_body, logged_in_student, logged_in_teacher, \
    get_detail_content
from django.utils import timezone


def teacher_many(request):
    if request.method == 'POST':  # Insert new teacher data
        body = get_body(request)
        required = ['username', 'password', 'fullname', 'email', 'birthday', 'account']
        verify = verify_data(body, required)
        if verify:
            return get_response(400, msg='(%s) is required in body.' % (', '.join(required)))

        try:
            Teacher.objects.create(
                username=body['username'],
                password=body['password'],
                fullname=body['fullname'],
                email=body['email'],
                birthday=body['birthday'],
                account=body['account']
            )

            return get_response(200)
        except IntegrityError:
            return get_response(400, msg='Username already exists. (%s)' %body['username'])
        except:
            traceback.print_exc()
            return get_response(500)
    elif request.method == 'PUT':
        teacher = logged_in_teacher(request)
        if teacher is None:
            return get_response(401)
        body = get_body(request)

        try:
            if 'password' in body: teacher.password = body['password']
            if 'fullname' in body: teacher.fullname = body['fullname']
            if 'birthday' in body: teacher.birthday = body['birthday']
            teacher.save()

            return get_response(200)
        except:
            traceback.print_exc()
            return get_response(500)
    else:
        return get_response(405, [request.method, 'POST', 'PUT'])


def teacher_one(request, teacher_id):
    if request.method == 'GET':
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            return get_response(200, to_json(teacher))
        except Teacher.DoesNotExist:
            return get_response(400, msg='Teacher id does not exist. (%s)' % teacher_id)
        except:
            traceback.print_exc()
            return get_response(500)
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
            traceback.print_exc()
            return get_response(500)
    else:
        return get_response(405, [request.method, 'POST'])


def logout(request):
    if request.method == 'GET':
        student = logged_in_student(request)
        teacher = logged_in_teacher(request)
        if teacher is None and student is None:
            return get_response(401)
        if 'student' in request.session:
            del request.session['student']
        if 'teacher' in request.session:
            del request.session['teacher']
        return get_response(200)
    else:
        return get_response(405, [request.method, 'GET'])


def student_many(request):
    if request.method == 'POST':
        body = get_body(request)
        required = ['username', 'password', 'fullname', 'email', 'birthday', 'image_id']
        verify = verify_data(body, required)
        if verify:
            return verify

        try:
            Student.objects.create(
                username=body['username'],
                password=body['password'],
                fullname=body['fullname'],
                email=body['email'],
                birthday=body['birthday'],
                image_id=body['image_id']
            )

            return get_response(200)
        except IntegrityError:
            return get_response(400, msg='Username already exists. (%s)' %body['username'])
        except:
            traceback.print_exc()
            return get_response(500)
    elif request.method == 'PUT':
        student = logged_in_student(request)
        if student is None:
            return get_response(401)
        body = get_body(request)

        try:
            if 'password' in body: student.password = body['password']
            if 'fullname' in body: student.fullname = body['fullname']
            if 'birthday' in body: student.birthday = body['birthday']
            if 'image_id' in body: student.image_id = body['image_id']
            student.save()

            return get_response(200)
        except:
            traceback.print_exc()
            return get_response(500)
    else:
        return get_response(405, [request.method, 'POST', 'PUT'])


def student_login(request):
    if request.method == 'POST':
        student = logged_in_student(request)
        if student is not None:
            return get_response(400, msg='User has already logged in. (%s)' % student.username)

        body = get_body(request)
        required = ['username', 'password']
        verify = verify_data(body, required)
        if verify:
            return verify

        try:
            student = Student.objects.get(username=body['username'], password=body['password'])
            request.session['student'] = student.id
            return get_response(200)
        except Student.DoesNotExist:
            return get_response(400, msg='Username or password does not match.')
        except:
            traceback.print_exc()
            return get_response(500)
    else:
        return get_response(405, [request.method, 'POST'])


def category_many(request):
    if request.method == 'GET':
        student = logged_in_student(request)
        teacher = logged_in_teacher(request)
        if student is None and teacher is None:
            return get_response(401)
        try:
            categories = Category.objects.all()
            data = []
            for category in categories:
                data.append(to_json(category))
            return get_response(200, data=data)
        except:
            traceback.print_exc()
            return get_response(500)
    else:
        return get_response(405, [request.method, 'GET'])


def content_many(request):
    if request.method == 'POST':
        teacher = logged_in_teacher(request)
        if teacher is None:
            return get_response(401)

        body = get_body(request)
        required = ['category', 'title', 'type', 'content', 'level']
        verify = verify_data(body, required)
        if verify:
            return verify

        try:
            Content.objects.create(
                category=Category.objects.get(id=body['category']),
                teacher=teacher,
                title=body['title'],
                type=body['type'],
                content=body['content'],
                level=body['level']
            )
            return get_response(200)
        except Category.DoesNotExist:
            return get_response(400, 'Category does not exist.')
        except:
            traceback.print_exc()
            return get_response(500)
    elif request.method == 'GET':
        student = logged_in_student(request)
        teacher = logged_in_teacher(request)
        if teacher is None and student is None:
            return get_response(401)

        data = {}
        categories = Category.objects.all()
        try:
            for t in ['0', '1', '2', '3']:
                contents_t = Content.objects.filter(type=int(t))
                data[t] = {}
                for cat in categories:
                    data[t][cat.english] = []
                    contents_c = contents_t.filter(category=cat)
                    for content in contents_c:
                        data[t][cat.english].append(to_json(content))
            return get_response(200, data=data)
        except:
            traceback.print_exc()
            return get_response(500)
    else:
        return get_response(405, [request.method, 'POST', 'GET'])


def content_one(request, content_id: int):
    if request.method == 'GET':
        student = logged_in_student(request)
        teacher = logged_in_teacher(request)
        if teacher is None and student is None:
            return get_response(401)

        try:
            content = Content.objects.get(id=content_id)
            data = get_detail_content(content)
            return get_response(200, data=data)
        except Content.DoesNotExist:
            return get_response(400, 'Content does not exist.')
        except:
            traceback.print_exc()
            return get_response(500)
    else:
        return get_response(405, [request.method, 'GET'])


def curriculum_many(request):
    if request.method == 'POST':
        student = logged_in_student(request)
        if student is None:
            return get_response(401)

        body = get_body(request)

        try:
            for content in body:
                curriculum, created = Curriculum.objects.get_or_create(
                    student=student,
                    content=Content.objects.get(id=content['content_id']),
                    defaults={"percentage": content['percentage']}
                )
                if not created:
                    curriculum.percentage = content['percentage']
                if 'score' in content:
                    # Save score and end datetime if student take test
                    curriculum.score = content['score']
                    curriculum.end_datetime = timezone.now()
                curriculum.save()

                return get_response(200)
        except Student.DoesNotExist:
            return get_response(400, 'Student does not exist.')
        except Content.DoesNotExist:
            return get_response(400, 'Content does not exist.')
        except:
            traceback.print_exc()
            return get_response(500)
    elif request.method == 'GET':
        student = logged_in_student(request)
        if student is None:
            return get_response(401)
        try:
            contents = Curriculum.objects.filter(student=student)
            data = [{'content_id': c.id, 'percentage': c.percentage, 'score': c.score} for c in contents]
            return get_response(200, data=data)
        except:
            traceback.print_exc()
            return get_response(500)
    else:
        return get_response(405, [request.method, 'POST', 'GET'])