from django.test import TestCase
from study.models import Teacher
from django.db.utils import IntegrityError


class TeacherTestCase(TestCase):
    def setUp(self):
        Teacher.objects.create(
            username='testcase1',
            password='testcase1',
            fullname='Test Case',
            email='test@case.com',
            birthday='2000-01-01'
        )

    def test_duplicated_username(self):
        with self.assertRaises(IntegrityError):
            Teacher.objects.create(username='testcase1',
                                   password='testcase1',
                                   fullname='Test Case',
                                   email='test@case.com',
                                   birthday='2000-01-01')