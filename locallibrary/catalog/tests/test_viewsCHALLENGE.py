from django.test import TestCase
from django.urls import reverse

# Create your tests here.

# Get user model from settings
from django.contrib.auth import get_user_model
User = get_user_model()

 # Required to grant the permission needed to add author.
from django.contrib.auth.models import Permission

from django.contrib.contenttypes.models import ContentType

from catalog.models import Author


class AuthorCreateViewTest(TestCase):
    """Test case for the AuthorCreate view (Created as Challenge)."""

    def setUp(self):
        # Create a user
        test_user = User.objects.create_user(
            username='test_user', password='some_password')

        content_typeAuthor = ContentType.objects.get_for_model(Author)
        permAddAuthor = Permission.objects.get(
            codename="add_author",
            content_type=content_typeAuthor,
        )

        test_user.user_permissions.add(permAddAuthor)
        test_user.save()