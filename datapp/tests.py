# datapp/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

from .models import Survey, Question, Option


class AddSurveyPageTest(TestCase):
    def test_add_survey_page_load(self):
        """
        假设 /create_survey/ 路由 -> name='add_survey'
        """
        response = self.client.get(
            reverse('add_survey'))  # 确保urls.py里 path('create_survey/', views.create_survey, name='add_survey')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Survey Title:')
        # ...


class AddSurveyFormTest(TestCase):
    def test_survey_form_submission(self):
        """
        测试提交表单
        """
        form_data = {
            'title': 'Test Survey',
            'description': 'Test desc',
            'startdate': '2025-01-01T00:00',
            'enddate': '2025-01-02T00:00',
        }
        response = self.client.post(reverse('add_survey'), data=form_data)
        # 假设提交后还是200 或者重定向
        self.assertEqual(response.status_code, 200)


class EditSurveyTest(TestCase):
    def setUp(self):
        # 创建Django默认用户
        self.user = User.objects.create_user(username='testuser', password='password123')

        # 用时区感知时间
        self.start_date = timezone.make_aware(
            datetime.datetime(2025, 1, 1, 0, 0),
            timezone.get_current_timezone()
        )
        self.end_date = self.start_date + datetime.timedelta(days=1)

        # 创建Survey
        self.survey = Survey.objects.create(
            createby=self.user,  # 必须是同一个User
            title="Test Survey",
            description="Test Description",
            startdate=self.start_date,
            enddate=self.end_date
        )

        # 创建问题、选项
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
        # 假设编辑成功后会重定向到 survey_detail
        self.assertRedirects(response, reverse('survey_detail', kwargs={'survey_id': self.survey.id}))

        # 检查数据库
        self.survey.refresh_from_db()
        self.assertEqual(self.survey.title, 'Updated Title')


class LoginTest(TestCase):
    def setUp(self):
        # 同样，用Django默认User
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_page_load(self):
        response = self.client.get(reverse('login'))  # 确保urls.py: path('login/', views.login_view, name='login')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_login_form_valid_submission(self):
        form_data = {'name': 'testuser', 'password': 'password123'}
        response = self.client.post(reverse('login'), data=form_data)
        # 假设登录后重定向到home
        self.assertRedirects(response, reverse('home'))

    def test_login_form_invalid_submission(self):
        form_data = {'name': 'wrong', 'password': 'wrong'}
        response = self.client.post(reverse('login'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error-message')

