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
        test_user1 = User.objects.create_user(
            username='testuser1', password='some_password')
        test_user1.save()


        # Create a user with add_author permission
        test_user2 = User.objects.create_user(
            username='testuser2', password='another_password')

        content_typeAuthor = ContentType.objects.get_for_model(Author)
        permAddAuthor = Permission.objects.get(
            codename="add_author",
            content_type=content_typeAuthor,
        )

        test_user2.user_permissions.add(permAddAuthor)
        test_user2.save()

# Test who has access
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-create'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/author/create/') # check

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='some_password')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 403)

    def test_if_logged_in_with_permission_add_author(self):
        login = self.client.login(username='testuser2', password='another_password')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)

# Test initial date
        
    def test_form_date_of_death_initially_11_11_2023(self):
        login = self.client.login(username='testuser2', password='another_password')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['form'].initial['date_of_death'], '11/11/2023')

# Test template used
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='another_password')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_form.html')

# Test where view redirects on success
    
    def test_redirects_to_book_detail_on_success(self):
        login = self.client.login(username='testuser2', password='another_password')
        response = self.client.post(reverse('author-create'), {
            "first_name": "test_first_name", "last_name": "test_last_name", "date_of_birth": "11/11/1953"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/catalog/author/'))
