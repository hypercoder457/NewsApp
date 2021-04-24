from django.test import TestCase

from users.models import CustomUser


class UsersModelTests(TestCase):
    def setUp(self) -> None:
        CustomUser.objects.create(
            email='rpshende60@gmail.com', first_name='Rudra', last_name='Shende')

    def test_user_str(self) -> None:
        user = CustomUser.objects.get(email='rpshende60@gmail.com')
        self.assertEqual(str(user), 'Rudra Shende')
