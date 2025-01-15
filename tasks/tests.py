from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from .models import Task

class TaskAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        
        # Generate JWT token for the user
        self.token = str(AccessToken.for_user(self.user))
        
        # Add token to authorization headers
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')
        
        # Create a sample task
        self.task = Task.objects.create(
            title="Sample Task",
            description="This is a test task",
            due_date="2025-01-20",
            completed=False
        )

    def test_get_task_list(self):
        """Test fetching the list of tasks."""
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_task_detail(self):
        """Test fetching a single task detail."""
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_create_task(self):
        """Test creating a new task."""
        data = {
            "title": "New Task",
            "description": "New task description",
            "due_date": "2025-01-25",
            "completed": False
        }
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().title, "New Task")

    def test_update_task(self):
        """Test updating an existing task."""
        data = {
            "title": "Updated Task Title",
            "description": "Updated task description",
            "due_date": "2025-02-01",
            "completed": True
        }
        response = self.client.put(f"/api/tasks/{self.task.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task Title")
        self.assertEqual(self.task.completed, True)

    def test_partial_update_task(self):
        """Test partially updating an existing task."""
        data = {"completed": True}
        response = self.client.patch(f"/api/tasks/{self.task.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.completed, True)

    def test_delete_task(self):
        """Test deleting a task."""
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)




from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from .models import Task
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken



class TaskFilterTests(APITestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="testuser", password="testpass")
        
        # Generate JWT token for the user
        self.token = str(AccessToken.for_user(self.user))
        
        # Add token to authorization headers
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')
        
        # Create some tasks for testing
        self.task1 = Task.objects.create(
            title="Task 1", completed=True, due_date="2025-01-15")
        self.task2 = Task.objects.create(
            title="Task 2", completed=False, due_date="2025-01-16")
        self.task3 = Task.objects.create(
            title="Task 3", completed=True, due_date="2025-01-16")
        self.task4 = Task.objects.create(
            title="Task 4", completed=False, due_date="2025-01-17")

    def test_filter_by_completed_true(self):
        # Test filtering by completed=True
        response = self.client.get('/api/tasks/', {'completed': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_titles = [task['title'] for task in response.data]
        self.assertIn("Task 1", task_titles)
        self.assertIn("Task 3", task_titles)
        self.assertNotIn("Task 2", task_titles)
        self.assertNotIn("Task 4", task_titles)

    def test_filter_by_completed_false(self):
        # Test filtering by completed=False
        response = self.client.get('/api/tasks/', {'completed': 'false'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_titles = [task['title'] for task in response.data]
        self.assertIn("Task 2", task_titles)
        self.assertIn("Task 4", task_titles)
        self.assertNotIn("Task 1", task_titles)
        self.assertNotIn("Task 3", task_titles)

    def test_filter_by_due_date(self):
        # Test filtering by due_date
        response = self.client.get('/api/tasks/', {'due_date': '2025-01-16'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_titles = [task['title'] for task in response.data]
        self.assertIn("Task 2", task_titles)
        self.assertIn("Task 3", task_titles)
        self.assertNotIn("Task 1", task_titles)
        self.assertNotIn("Task 4", task_titles)

    def test_filter_by_completed_and_due_date(self):
        # Test filtering by both completed and due_date
        response = self.client.get('/api/tasks/', {'completed': 'true', 'due_date': '2025-01-16'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_titles = [task['title'] for task in response.data]
        self.assertIn("Task 3", task_titles)
        self.assertNotIn("Task 1", task_titles)
        self.assertNotIn("Task 2", task_titles)
        self.assertNotIn("Task 4", task_titles)

    def test_filter_by_no_matching_results(self):
        # Test filtering when no tasks match the filter
        response = self.client.get('/api/tasks/', {'completed': 'false', 'due_date': '2025-01-15'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_filter_by_invalid_date(self):
        # Test filtering by an invalid date
        response = self.client.get('/api/tasks/', {'due_date': 'invalid-date'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
