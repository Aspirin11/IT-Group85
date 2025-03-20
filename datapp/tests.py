from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

from .models import Survey, Question, Option


class AddSurveyPageTest(TestCase):
    def test_add_survey_page_load(self):

        response = self.client.get(
            reverse('add_survey'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Survey Title:')
        # ...


class AddSurveyFormTest(TestCase):
    def test_survey_form_submission(self):

        form_data = {
            'title': 'Test Survey',
            'description': 'Test desc',
            'startdate': '2025-01-01T00:00',
            'enddate': '2025-01-02T00:00',
        }
        response = self.client.post(reverse('add_survey'), data=form_data)
        self.assertEqual(response.status_code, 200)


class EditSurveyTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.start_date = timezone.make_aware(
            datetime.datetime(2025, 1, 1, 0, 0),
            timezone.get_current_timezone()
        )
        self.end_date = self.start_date + datetime.timedelta(days=1)

        self.survey = Survey.objects.create(
            createby=self.user,
            title="Test Survey",
            description="Test Description",
            startdate=self.start_date,
            enddate=self.end_date
        )

        self.question = Question.objects.create(
            survey=self.survey,
            question_text="What is your name?",
            type=0,
            isrequired=True
        )
        Option.objects.create(question=self.question, optiontext="Alice")
        Option.objects.create(question=self.question, optiontext="Bob")

    def test_edit_survey_page_load(self):
        response = self.client.get(reverse('edit_survey', kwargs={'survey_id': self.survey.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Survey Title:')

    def test_edit_survey_form_submission(self):
        form_data = {
            'title': 'Updated Title',
            'description': 'Updated desc',
            'startdate': '2025-02-01T00:00',
            'enddate': '2025-02-02T00:00',
            'question_text[]': ['What is your name?'],
            'question_type[]': ['0'],
            'is_required[]': ['1'],
            'options[]': ['Alice|Bob']
        }
        response = self.client.post(reverse('edit_survey', kwargs={'survey_id': self.survey.id}), data=form_data)
        self.assertRedirects(response, reverse('survey_detail', kwargs={'survey_id': self.survey.id}))

        self.survey.refresh_from_db()
        self.assertEqual(self.survey.title, 'Updated Title')


class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_page_load(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_login_form_valid_submission(self):
        form_data = {'name': 'testuser', 'password': 'password123'}
        response = self.client.post(reverse('login'), data=form_data)
        self.assertRedirects(response, reverse('home'))

    def test_login_form_invalid_submission(self):
        form_data = {'name': 'wrong', 'password': 'wrong'}
        response = self.client.post(reverse('login'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error-message')

