from django.test import TestCase
from django.contrib.auth import get_user_model


USER_MODEL = get_user_model()



class TestCaseBase(TestCase):

    def setUp(self) -> None:
        self.user = USER_MODEL.objects.create(
            username="admin",
            email='admin@gmail.com',
            password='adminadmin'
        )
    