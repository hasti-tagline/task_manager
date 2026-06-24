

# Create your tests here.
from django.test import TestCase
from accounts.models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="hasti",
            password="1234"
        )

        self.assertEqual(user.username, "hasti")