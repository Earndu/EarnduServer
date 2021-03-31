import json

from django.shortcuts import render

from study.models import Teacher, Student, Content, Category, Curriculum
from study.forms import ContentForm, ContentFormMobile
import traceback
from django.db.utils import IntegrityError
from study.utils import get_response, verify_data, to_json, get_body, logged_in_student, logged_in_teacher, \
    get_detail_content
from django.utils import timezone
import logging
import re
import base64

logger = logging.getLogger('std.file')


def student_total(request):
    if request.method == 'POST':
        body = get_body(request)
        required = ['username', 'password']
        verify = verify_data(body, required)
        if verify:
            return get_response(logger, request, 400, msg='(%s) is required in body.' % (', '.join(required)))

        wish_list = body['wish_list'] if 'wish_list' in body else []
        curriculums = body['curriculum'] if 'curriculum' in body else []


        try:
            student = Student.objects.get(username=body['username'], password=body['password'])

            for cur in curriculums:
                curriculum, created = Curriculum.objects.get_or_create(
                    student=student,
                    content=Content.objects.get(id=cur['content_id']),
                    defaults={"percentage": cur['percentage']}
                )
                if not created:
                    curriculum.percentage = cur['percentage']
                if 'score' in cur:
                    # Save score and end datetime if student take test
                    curriculum.score = cur['score']
                    curriculum.end_datetime = cur['end_datetime'] \
                        if 'end_datetime' in cur \
                        else timezone.now()
                curriculum.save()

            categories = Category.objects.all()

            content_data = {
                t:{
                    cat.english: [
                        to_json(content) for content in Content.objects.filter(type=int(t), category=cat)
                    ] for cat in categories
                } for t in ['0', '1', '2', '3']
            }

            wish_list_data = [get_detail_content(Content.objects.get(id=c_id)) for c_id in wish_list]
            curriculum_data = [to_json(cur) for cur in Curriculum.objects.filter(student=student)]

            return get_response(logger, request, 200, data={
                'user_data': to_json(student),
                'content_list': content_data,
                'wish_list': wish_list_data,
                'curriculum': curriculum_data
            }, student_id=student.id)
        except Student.DoesNotExist:
            return get_response(logger, request, 400, msg='Username or password does not match.')
        except:
            traceback.print_exc()
            return get_response(logger, request, 500)
    else:
        return get_response(logger, request, 405, data=[request.method, 'POST'])


def teacher_many(request):
    if request.method == 'POST':  # Insert new teacher data
        body = get_body(request)
        required = ['username', 'password', 'fullname', 'email', 'birthday', 'account']
        verify = verify_data(body, required)
        if verify:
            return get_response(logger, request, 400, msg='(%s) is required in body.' % (', '.join(required)))

        try:
            Teacher.objects.create(
                username=body['username'],
                password=body['password'],
                fullname=body['fullname'],
                email=body['email'],
                birthday=body['birthday'],
                account=body['account']
            )

            return get_response(logger, request, 200)
        except IntegrityError:
            return get_response(logger, request, 400, msg='Username already exists. (%s)' %body['username'])
        except:
            traceback.print_exc()
            return get_response(logger, request, 500)
    elif request.method == 'PUT':
        teacher = logged_in_teacher(request)
        if teacher is None:
            return get_response(logger, request, 401)
        body = get_body(request)

        try:
            if 'password' in body: teacher.password = body['password']
            if 'fullname' in body: teacher.fullname = body['fullname']
            if 'birthday' in body: teacher.birthday = body['birthday']
            teacher.save()

            return get_response(logger, request, 200, teacher_id=teacher.id)
        except:
            traceback.print_exc()
            return get_response(logger, request, 500, teacher_id=teacher.id)
    else:
        return get_response(logger, request, 405, data=[request.method, 'POST', 'PUT'])


def teacher_login(request):
    if request.method == 'POST':
        teacher_id = request.session.get('teacher')
        if teacher_id:
            teacher = Teacher.objects.get(id=teacher_id)
            return get_response(logger, request, 400, msg='User has already logged in. (%s)' % teacher.username)

        body = get_body(request)
        required = ['username', 'password']
        verify = verify_data(body, required)
        if verify:
            return get_response(logger, request, 400, msg='(%s) is required in body.' % (', '.join(required)))

        try:
            teacher = Teacher.objects.get(username=body['username'], password=body['password'])
            request.session['teacher'] = teacher.id
            return get_response(logger, request, 200, teacher_id=teacher.id)
        except Teacher.DoesNotExist:
            return get_response(logger, request, 400, msg='Username or password does not match.')
        except:
            traceback.print_exc()
            return get_response(logger, request, 500)
    else:
        return get_response(logger, request, 405, data=[request.method, 'POST'])


def logout(request):
    if request.method == 'GET':
        student = logged_in_student(request)
        teacher = logged_in_teacher(request)
        if teacher is None and student is None:
            return get_response(logger, request, 401)
        if 'student' in request.session:
            del request.session['student']
        if 'teacher' in request.session:
            del request.session['teacher']
        return get_response(logger, request, 200,
                            teacher_id=teacher.id if teacher is not None else None,
                            student_id=student.id if student is not None else None)
    else:
        return get_response(logger, request, 405, data=[request.method, 'GET'])


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

            return get_response(logger, request, 200)
        except IntegrityError:
            return get_response(logger, request, 400, msg='Username already exists. (%s)' %body['username'])
        except:
            traceback.print_exc()
            return get_response(logger, request, 500)
    elif request.method == 'PUT':
        student = logged_in_student(request)
        if student is None:
            return get_response(logger, request, 401)
        body = get_body(request)

        try:
            if 'password' in body: student.password = body['password']
            if 'fullname' in body: student.fullname = body['fullname']
            if 'birthday' in body: student.birthday = body['birthday']
            if 'image_id' in body: student.image_id = body['image_id']
            student.save()

            return get_response(logger, request, 200, student_id=student.id)
        except:
            traceback.print_exc()
            return get_response(logger, request, 500, student_id=student.id)
    else:
        return get_response(logger, request, 405, data=[request.method, 'POST', 'PUT'])


def student_login(request):
    if request.method == 'POST':
        student = logged_in_student(request)
        if student is not None:
            return get_response(logger, request, 400, msg='User has already logged in. (%s)' % student.username)

        body = get_body(request)
        required = ['username', 'password']
        verify = verify_data(body, required)
        if verify:
            return verify

        try:
            student = Student.objects.get(username=body['username'], password=body['password'])
            request.session['student'] = student.id
            return get_response(logger, request, 200, student_id=student.id)
        except Student.DoesNotExist:
            return get_response(logger, request, 400, msg='Username or password does not match.')
        except:
            traceback.print_exc()
            return get_response(logger, request, 500)
    else:
        return get_response(logger, request, 405, data=[request.method, 'POST'])


def category_many(request):
    if request.method == 'GET':
        student = logged_in_student(request)
        teacher = logged_in_teacher(request)
        if student is None and teacher is None:
            return get_response(logger, request, 401)
        try:
            categories = Category.objects.all()
            data = []
            for category in categories:
                data.append(to_json(category))
            return get_response(logger, request, 200, data=data,
                                teacher_id=teacher.id if teacher is not None else None,
                                student_id=student.id if student is not None else None)
        except:
            traceback.print_exc()
            return get_response(logger, request, 500,
                                teacher_id=teacher.id if teacher is not None else None,
                                student_id=student.id if student is not None else None)
    else:
        return get_response(logger, request, 405, data=[request.method, 'GET'])


def content_many(request):
    if request.method == 'POST':
        teacher = logged_in_teacher(request)
        if teacher is None:
            return get_response(logger, request, 401)

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
                level=body['level'],
                res_image=body['res_image'] if 'res_image' in body else None,
                res_sound=body['res_sound'] if 'res_sound' in body else None
            )
            return get_response(logger, request, 200, teacher_id=teacher.id)
        except Category.DoesNotExist:
            return get_response(logger, request, 400, msg='Category does not exist.', teacher_id=teacher.id)
        except:
            traceback.print_exc()
            return get_response(logger, request, 500, teacher_id=teacher.id)
    elif request.method == 'GET':
        student = logged_in_student(request)
        teacher = logged_in_teacher(request)
        if teacher is None and student is None:
            return get_response(logger, request, 401)

        data = {}
        categories = Category.objects.all()
        try:
            for t in ['0', '1', '2']:
                contents_t = Content.objects.filter(type=int(t))
                data[t] = {}
                for cat in categories:
                    data[t][cat.english] = []
                    contents_c = contents_t.filter(category=cat)
                    for content in contents_c:
                        data[t][cat.english].append(to_json(content))
            return get_response(logger, request, 200, data=data,
                                teacher_id=teacher.id if teacher is not None else None,
                                student_id=student.id if student is not None else None)
        except:
            traceback.print_exc()
            return get_response(logger, request, 500,
                                teacher_id=teacher.id if teacher is not None else None,
                                student_id=student.id if student is not None else None)
    else:
        return get_response(logger, request, 405, data=[request.method, 'POST', 'GET'])


def content_one(request, content_id: int):
    if request.method == 'GET':
        student = logged_in_student(request)
        teacher = logged_in_teacher(request)
        if teacher is None and student is None:
            return get_response(logger, request, 401)

        try:
            content = Content.objects.get(id=content_id)
            data = get_detail_content(content)
            return get_response(logger, request, 200, data=data,
                                teacher_id=teacher.id if teacher is not None else None,
                                student_id=student.id if student is not None else None)
        except Content.DoesNotExist:
            return get_response(logger, request, 400, msg='Content does not exist.',
                                teacher_id=teacher.id if teacher is not None else None,
                                student_id=student.id if student is not None else None)
        except:
            traceback.print_exc()
            return get_response(logger, request, 500,
                                teacher_id=teacher.id if teacher is not None else None,
                                student_id=student.id if student is not None else None)
    elif request.method == 'PUT':
        teacher = logged_in_teacher(request)
        if teacher is None:
            return get_response(logger, request, 401)

        body = get_body(request)
        try:
            content = Content.objects.get(id=content_id)
            if content.teacher_id != teacher.id:
                return get_response(logger, request, 401, msg='Writer of content and user logged in does not match.')

            if 'category' in body: content.category_id = body['category']
            if 'title' in body: content.title = body['title']
            if 'type' in body: content.type = body['type']
            if 'content' in body: content.content = body['content']
            if 'level' in body: content.level = body['level']
            if 'res_image' in body: content.res_image = body['res_image']
            if 'res_sound' in body: content.res_sound = body['res_sound']
            content.save()

            return get_response(logger, request, 200, teacher_id=teacher.id)
        except Category.DoesNotExist:
            return get_response(logger, request, 400, msg='Category does not exist.', teacher_id=teacher.id)
        except:
            traceback.print_exc()
            return get_response(logger, request, 500, teacher_id=teacher.id)
    else:
        return get_response(logger, request, 405, data=[request.method, 'GET', 'PUT'])


def curriculum_many(request):
    if request.method == 'POST':
        student = logged_in_student(request)
        if student is None:
            return get_response(logger, request, 401)

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
                    curriculum.end_datetime = content['end_datetime'] \
                        if 'end_datetime' in content \
                        else timezone.now()
                curriculum.save()

            return get_response(logger, request, 200, student_id=student.id)
        except Student.DoesNotExist:
            return get_response(logger, request, 400, msg='Student does not exist.', student_id=student.id)
        except Content.DoesNotExist:
            return get_response(logger, request, 400, msg='Content does not exist.', student_id=student.id)
        except:
            traceback.print_exc()
            return get_response(logger, request, 500, student_id=student.id)
    elif request.method == 'GET':
        student = logged_in_student(request)
        if student is None:
            return get_response(logger, request, 401)
        try:
            contents = Curriculum.objects.filter(student=student)
            data = [to_json(c) for c in contents]
            return get_response(logger, request, 200, data=data, student_id=student.id)
        except:
            traceback.print_exc()
            return get_response(logger, request, 500, student_id=student.id)
    else:
        return get_response(logger, request, 405, data=[request.method, 'POST', 'GET'])


def content_add(request, client=None):
    if request.method == 'POST':
        try:
            body = request.POST
            images = request.FILES.getlist('images')
            voice = request.FILES.get('voice')
            teacher = Teacher.objects.get(username=body['username'], password=body['password'])
            content = body['content']
            # content = re.sub('\n|\r', '', content)
            # content = re.sub('</{0,1}br/{0,1}>', '\n', content)

            b64 = '<SEP>'.join([str(base64.b64encode(image.file.read()))[2:-1] for image in images])
            b64_voice = str(base64.b64encode(voice.file.read()))[2:-1] if voice is not None else None

            Content.objects.create(
                category_id=body['category'],
                teacher=teacher,
                title=body['title'],
                type=body['type'],
                content=content,
                level=body['level'],
                res_image=b64,
                res_sound=b64_voice
            )
            context = {'title': body['title'], 'form': ContentFormMobile() if client == 'm' else ContentForm()}
            return render(request, 'study/add_content.html', context)
        except Teacher.DoesNotExist:
            return get_response(logger, request, 400, msg='Username or password does not match.')
        except:
            traceback.print_exc()
            return get_response(logger, request, 500)
    else:
        context = {'form': ContentFormMobile() if client == 'm' else ContentForm()}
        return render(request, 'study/add_content.html', context)