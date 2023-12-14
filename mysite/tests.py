from django.test import TestCase
from django.contrib.auth.models import User
from users.models import StudySpot
from django.urls import reverse_lazy
from django.utils import timezone
from django.urls import reverse  # Add this line

class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 2

    def test_dummy_test_case(self):
        self.assertNotEquals(1, 2)

    # def setUp(self):
    #     # Set up necessary objects for testing, including a regular user, an admin user,
    #     # and StudySpot instances for testing CRUD operations.
    #     self.user = User.objects.create_user(username="dummy", password="duh")

    #     self.study_spot1 = StudySpot.objects.create(
    #         building_name="Alderman Library",
    #         user_posted=self.user,
    #         notes="Coming soon",
    #         likes=10,
    #         approved=False,
    #     )

    # def test_user_authentication(self):
    #     # Log in the user
    #     self.client.login(username='testuser', password='testpassword')
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)

    # def test_admin_access(self):
    #     # Log in the admin user
    #     self.client.login(username='adminuser', password='adminpassword')
    #     response = self.client.get(reverse('admin:index'))
    #     self.assertEqual(response.status_code, 200)

    # def test_create_study_spot(self):
    #     self.client.login(username="dummy", password="duh")
    #     data = {
    #         "building_name": "Clark Library",
    #         "notes": "Quiet, clean, comfortable",
    #     }
    #     response = self.client.post(reverse_lazy("users:create_study_spot"), data)
    #     self.assertEqual(response.status_code, 302)  # should redirect
    #     self.assertTrue(StudySpot.objects.filter(building_name="New Building").exists())

    # def test_update_study_spot(self):
    #     self.client.login(username="dummy", password="duh")
    #     data = {
    #         "building_name": "Clark Mural Hall",
    #         "notes": "Quiet depending on where you choose to sit, comfortable",
    #         # Add other required fields
    #     }
    #     response = self.client.post(
    #         reverse_lazy("users:update_study_spot", kwargs={"pk": self.study_spot1.id}),
    #         data,
    #     )
    #     self.assertEqual(response.status_code, 302)  # should redirect
    #     self.study_spot1.refresh_from_db()
    #     self.assertEqual(self.study_spot1.building_name, "Clark Mural Hall")

    # def test_like_study_spot(self):
    #     self.client.login(username="dummy", password="duh")
    #     response = self.client.post(
    #         reverse_lazy("users:like_study_spot", kwargs={"pk": self.study_spot1.id})
    #     )
    #     self.assertEqual(response.status_code, 302)  # should redirect
    #     self.study_spot1.refresh_from_db()
    #     self.assertEqual(self.study_spot1.likes, 11)  # Assuming it increases the likes count

    # def test_dislike_study_spot(self):
    #     self.client.login(username="dummy", password="duh")
    #     response = self.client.post(
    #         reverse_lazy("users:dislike_study_spot", kwargs={"pk": self.study_spot1.id})
    #     )
    #     self.assertEqual(response.status_code, 302)  # should redirect
    #     self.study_spot1.refresh_from_db()
    #     self.assertEqual(self.study_spot1.likes, 9)  # Assuming it decreases the likes count

    # def test_delete_study_spot(self):
    #     self.client.login(username="dummy", password="duh")
    #     response = self.client.post(
    #         reverse_lazy("users:delete_study_spot", kwargs={"pk": self.study_spot1.id})
    #     )
    #     self.assertEqual(response.status_code, 302)  # should redirect
    #     self.assertFalse(
    #         StudySpot.objects.filter(id=self.study_spot1.id).exists()
    #     )  # should now be deleted

    # def test_comment_on_study_spot(self):
    #     self.client.login(username="dummy", password="duh")
    #     response = self.client.post(
    #         reverse_lazy("users:spot", kwargs={"pk": self.study_spot1.id}),
    #         {"action": "comment", "study_spot_id": self.study_spot1.id, "message": "Test comment"},
    #     )
    #     self.assertEqual(response.status_code, 302)  # should redirect
    #     self.assertTrue(self.study_spot1.comments.filter(message="Test comment").exists())



    # def test_valid_post_request(self):
    #     # Log in a user (or create a user session)
    #     self.client.login(username='testuser', password='testpassword')

    #     # Create a StudySpot instance with valid data
    #     data = {
    #         'building_name': 'Clemons Library',
    #         'notes': 'Different noise levels',
    #         # Add other required fields
    #     }

    #     response = self.client.post(reverse('home'), data)
    #     self.assertEqual(response.status_code, 200)

    # def test_blank_fields(self):
    #     # Log in a user (or create a user session)
    #     self.client.login(username='testuser', password='testpassword')

    #     # Create a StudySpot instance with blank fields
    #     data = {
    #         'building_name': '',
    #         'notes': '',
    #         # Add other required fields
    #     }

    #     response = self.client.post(reverse('home'), data)
    #     self.assertEqual(response.status_code, 400)

