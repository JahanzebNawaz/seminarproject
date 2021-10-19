from .testcasebase import USER_MODEL, TestCaseBase
from django.contrib.auth import authenticate, get_user_model
import unittest

USER_MODEL = get_user_model()



class UserModelTests(TestCaseBase):

    DATA = {
        "username": "demo",
        "email": "demo@gmail.com",
        "password": "adminadmin",
        "date_of_birth": "1990-12-12",
        "phone_no": "2020202020220",
        "age": "24",
        "gender": "Male",
        "address": "Skane Malmo",
        "credit_card": None,
        "is_verified": False,
    }

    def setUp(self) -> None:
        self.data = self.DATA
        return super().setUp()

    def test_create_user(self):
        self.data['email'] = 'demo1@gmail.com'
        self.data['username'] = 'demo1'
        user = USER_MODEL.objects.create_user(**self.data)
        user_obj = USER_MODEL.objects.get(username='demo1')
        self.assertEqual(user.pk, user_obj.pk)
    
    @unittest.expectedFailure
    def test_create_user_without_username(self):
        del self.data['username']
        del self.data['email']
        user = USER_MODEL.objects.create_user(**self.data)
        user_obj = USER_MODEL.objects.get(phone_no=self.data['phone_no'])
        self.assertEqual(user.pk, user_obj.pk)

    def test_correct_user(self):
        self.create_new_user()
        user = authenticate(email=self.data['email'], password=self.data['password'])
        self.assertTrue((user is not None) and user.is_authenticated)

    @unittest.expectedFailure
    def test_wrong_user(self):
        self.create_new_user()
        user = authenticate(email='wrong', password=self.data['password'])
        # print(user)
        self.assertFalse(user is not None and user.is_authenticated)

    def test_count_user(self):
        count = USER_MODEL.objects.count()
        last = USER_MODEL.objects.last().pk
        self.assertEqual(count, last)
    

    def create_new_user(self):
        user = USER_MODEL.objects.create_user(**self.data)
        return user