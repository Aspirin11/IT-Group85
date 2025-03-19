import json

from .models import Survey, Question, Option, Answer, User, Response
from .models import Survey, Question, Answer, Response
from django.shortcuts import get_object_or_404, render
import matplotlib.pyplot as plt
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from .models import Survey, Question, Answer, Response, Option
from django.utils.timezone import now
from .models import Survey, Question, Option, Response, Answer
from collections import Counter
from django.http import HttpResponse
# from pyecharts import options as opts
from pyecharts.charts import Pie
from .models import Survey, Question, Answer, Option
from .models import Survey
from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, User
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from django import forms
from .models import *
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404



class LoginForm(forms.Form):
    name = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={'class': "form-control", 'placeholder': "Enter your username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': "form-control", 'placeholder': "Enter your password"}, render_value=True),
    )



from django import forms
from django.core.exceptions import ValidationError
from .models import User

class RegisterForm(forms.Form):
    name = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={'class': "form-control", 'placeholder': "Enter your username"}),
        max_length=16,
        error_messages={
            'required': 'Username is required',
            'max_length': 'Username cannot be longer than 16 characters'
        }
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={'class': "form-control", 'placeholder': "Enter your email"}),
        max_length=20,
        error_messages={
            'required': 'Email is required',
            'invalid': 'Please enter a valid email address',
            'max_length': 'Email cannot be longer than 20 characters'
        }
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': "form-control", 'placeholder': "Enter your password"}),
        error_messages={
            'required': 'Password is required',
        }
    )
    password1 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={'class': "form-control", 'placeholder': "Confirm your password"}),
        error_messages={
            'required': 'Please confirm your password',
        }
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if User.objects.filter(name=name).exists():
            raise ValidationError("This username is already registered")
        return name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')

        if password and password1 and password != password1:
            raise ValidationError("Passwords do not match")

        return cleaned_data



def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, "login.html", {"form": form})

    name = form.cleaned_data['name']
    password = form.cleaned_data['password']

    user = User.objects.filter(name=name).first()

    if not user:
        return render(request, "login.html", {"form": form, "error": "User does not exist"})

    if not user.check_password(password):
        return render(request, "login.html", {"form": form, "error": "Incorrect password"})

    request.session['info'] = {"name": name}
    request.session.set_expiry(6000)

    return redirect('/create_survey/')




def logout(request):
    request.session.clear()
    return redirect('/login/')


def res(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "res.html", {"form": form})
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['password1']

            if password == password1:
                user = User(name=name, password=password, email=email)
                user.save()
                return redirect("/login/")  # 注册成功，不传递错误消息
            else:
                error = "Passwords do not match. Please try again."  # 错误信息传递到模板
                return render(request, "res.html", {"form": form, "error": error})
        else:
            error = "Please fill in all fields correctly."  # 错误信息传递到模板
            return render(request, "res.html", {"form": form, "error": error})

    return render(request, "res.html", {"error": None})


def change_password(request):
    if request.method == "POST":
        name = request.session.get("info_dict", {}).get("name")
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        email = request.POST.get("email")

        if name:
            if not old_password or not new_password and email:
                user = User.objects.filter(name=name).first()
                user.email = email
                user.save()
                return redirect("/create_survey/")
            else:
                user = User.objects.filter(name=name).first()
                if user and check_password(old_password, user.password):
                    user.password = make_password(new_password)
                    user.save()
                    messages.success(request, "Password changed successfully")
                    return redirect("/create_survey/")
                else:
                    messages.error(request, "Incorrect old password")

    return render(request, "change.html")


def create_survey(request):
    if request.method == "POST":

        username = request.info_dict.get("name", "")
        user = User.objects.filter(name=username).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        survey_title = request.POST.get("title", "")
        survey_description = request.POST.get("description", "")
        start_date = request.POST.get("startdate", None)
        end_date = request.POST.get("enddate", None)
        try:
            survey = Survey.objects.create(
                title=survey_title,
                description=survey_description,
                createby=user,
                startdate=start_date,
                enddate=end_date,
                status=0,
            )
            if survey:
                questions = Question.objects.filter(survey=survey).order_by('order')
                if request.method == "POST":
                    question_texts = request.POST.getlist("question_text[]")
                    question_types = request.POST.getlist("question_type[]")
                    is_required_list = request.POST.getlist("is_required[]")
                    options_data = request.POST.getlist("options[]")
                    kept_question_ids = request.POST.getlist("kept_question_ids[]")

                    kept_question_ids = [qid for qid in kept_question_ids if qid.isdigit()]

                    Question.objects.filter(survey=survey).exclude(id__in=kept_question_ids).delete()
                    for index, question_text in enumerate(question_texts):
                        is_required = int(is_required_list[index]) if index < len(is_required_list) else 0  # Default to 0
                        question, created = Question.objects.update_or_create(
                            id=kept_question_ids[index] if index < len(kept_question_ids) else None,
                            defaults={
                                'survey': survey,
                                'question_text': question_text,
                                'type': int(question_types[index]),
                                'order': index + 1,
                                'isrequired': is_required,
                            }
                        )

                        if question.type in [0, 1]: 
                            options_for_question = options_data[index].split('|') if index < len(options_data) else []
                            question.option_set.all().delete()
                            for option_order, option_text in enumerate(options_for_question):
                                Option.objects.create(
                                    question=question,
                                    optiontext=option_text.strip(),
                                    order=option_order + 1
                                )
            return redirect("surveys")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, "add_survey.html")


def survey_list(request):
    username = request.info_dict.get("name", "")
    user = User.objects.filter(name=username).first()
    surveys = Survey.objects.filter(createby=user)
    return render(request, "survey_list.html", {"surveys": surveys})


def delete_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    survey.delete()
    return redirect("survey_list")

def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = Question.objects.filter(survey=survey).order_by('order')

    if request.method == "POST":

        survey_title = request.POST.get("title", "")
        survey_description = request.POST.get("description", "")
        start_date = request.POST.get("startdate", None)
        end_date = request.POST.get("enddate", None)

        survey.title = survey_title
        survey.description = survey_description
        survey.start_date = start_date
        survey.end_date = end_date
        survey.save()

        # Update questions
        question_texts = request.POST.getlist("question_text[]")
        question_types = request.POST.getlist("question_type[]")
        is_required_list = request.POST.getlist("is_required[]")
        options_data = request.POST.getlist("options[]")
        print(f"options_data is {options_data}")
        kept_question_ids = request.POST.getlist("kept_question_ids[]")

        kept_question_ids = [qid for qid in kept_question_ids if qid.isdigit()]

        Question.objects.filter(survey=survey).exclude(id__in=kept_question_ids).delete()
        for index, question_text in enumerate(question_texts):
            is_required = int(is_required_list[index]) if index < len(is_required_list) else 0  # Default to 0
            question, created = Question.objects.update_or_create(
                id=kept_question_ids[index] if index < len(kept_question_ids) else None,
                defaults={
                    'survey': survey,
                    'question_text': question_text,
                    'type': int(question_types[index]),
                    'order': index + 1,
                    'isrequired': is_required,
                }
            )

            if question.type in [0, 1]: 
                options_for_question = options_data[index].split('|') if index < len(options_data) else []
                print(f"options_for_question is {str(options_for_question)}")
                question.option_set.all().delete()
                # print(f"options_data is {options_data}")
                for option_order, option_text in enumerate(options_for_question):
                    Option.objects.create(
                        question=question,
                        optiontext=option_text.strip(),
                        order=option_order + 1
                    )

    context = {
        'survey': survey,
        'questions': questions,
    }
    return render(request, 'edit_survey.html', context)




from django.contrib import messages
def fill_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    username = request.info_dict.get("name", "")
    user = User.objects.filter(name=username).first()

    if request.method == "POST":
        anonymous = request.POST.get("anonymous")
        print(anonymous)
        if anonymous == 1:
            response = Response.objects.create(survey=survey)
        else:
            response = Response.objects.create(user=user, survey=survey)
       
        answers_to_create = []
        for key, value in request.POST.items():
            if key.startswith("answers["):
                question_id = key[8:-1]
                question = Question.objects.get(id=question_id)
                if question.type == 2:    # Text question
                    answers_to_create.append(
                        Answer(response=response, question=question, answerertext=value))
                elif question.type == 1:  # Multiple choice
                    option_ids = request.POST.getlist(key)
                    for option_id in option_ids:
                        selected_option = Option.objects.get(id=option_id)
                        answers_to_create.append(
                            Answer(response=response, question=question, selectedoption=selected_option))
                else:                     # Single choice
                    selected_option = Option.objects.get(id=value)
                    answers_to_create.append(
                        Answer(response=response, question=question, selectedoption=selected_option))
        Answer.objects.bulk_create(answers_to_create)  # Bulk save answers
        
        return redirect("survey_list")

    response = Response.objects.filter(user=user, survey=survey).first()

    if response:
        messages.error(request, "You have already participated in this survey")  
        return redirect("surveys")

    if survey.enddate < now():
        messages.error(request, "This survey has ended")
        return redirect("surveys")

    questions = Question.objects.filter(survey=survey).prefetch_related("option_set")
    return render(request, "fill_survey.html", {"survey": survey, "questions": questions})


def surveys(request):
    surveys = Survey.objects.all()
    current_time = now()
    return render(request, "surveys.html", {"surveys": surveys, "current_time": current_time})

def survey_analysis(request):
    """View for displaying survey analysis dashboard with visualizations"""
    username = request.session.get('info', {}).get('name', '')
    user = User.objects.filter(name=username).first()
    
    # Get all surveys or filter by user if needed
    if user:
        surveys = Survey.objects.all()
        
        # Summary statistics
        total_surveys = surveys.count()
        total_responses = Response.objects.count()
        avg_responses_per_survey = total_responses / total_surveys if total_surveys > 0 else 0
        
        # Get response counts for each survey for bar chart
        survey_data = []
        for survey in surveys:
            response_count = Response.objects.filter(survey=survey).count()
            survey_data.append({
                'id': survey.id,
                'title': survey.title,
                'response_count': response_count
            })
        
        # Get question type distribution for pie chart
        question_types = Question.objects.values('type').annotate(count=Count('id'))
        question_type_data = []
        for item in question_types:
            type_name = dict(Question.QUESTION_TYPE_CHOICES).get(item['type'])
            question_type_data.append({
                'type': type_name,
                'count': item['count']
            })
        
        # Get recent responses for timeline
        recent_responses = Response.objects.order_by('-datesubmitted')[:10]
        
        context = {
            'total_surveys': total_surveys,
            'total_responses': total_responses,
            'avg_responses_per_survey': round(avg_responses_per_survey, 2),
            'survey_data': survey_data,
            'question_type_data': question_type_data,
            'recent_responses': recent_responses,
        }
        
        return render(request, "survey_analysis.html", context)
    
    # If user not found, redirect to login
    return redirect('/login/')

import pyecharts.options as opts
from pyecharts.globals import ThemeType


def survey_statistics(request, survey_id):
    try:
        survey = Survey.objects.get(pk=survey_id)
        questions = Question.objects.filter(survey=survey)
        total_users = User.objects.all().count()
        completed_users = Response.objects.filter(survey=survey).count()

        completion_rate = (completed_users / total_users * 100) if total_users > 0 else 0

        question_statistics = []

        for question in questions:
            question_data = {
                "question_text": question.question_text,
                "type": question.get_type_display(),
                "is_required": question.isrequired,
            }

            if question.type in [0,1]:
                print("走到这里了",f"{question.type}")
                options = Option.objects.filter(question=question)
                option_data = []
                pie_chart_data = []

                for option in options:
                    count = Answer.objects.filter(
                        question=question, selectedoption=option).count()
                    option_data.append(
                        {"option_text": option.optiontext, "count": count})
                    pie_chart_data.append((option.optiontext, count))

                question_data["options"] = option_data

                # # 检查 pie_chart_data 是否为空
                if pie_chart_data:
                    pie = (
                        Pie(init_opts=opts.InitOpts( theme=ThemeType.LIGHT,width='100%', height='20vh'))
                        .add("", pie_chart_data,
                             radius=["50%", "90%"],
                             center=["50%", "50%"],
                             )
                        .set_global_opts(
                            title_opts=opts.TitleOpts(title=""),
                            legend_opts=opts.LegendOpts(
                                orient="vertical", pos_top="15%", pos_left="2%")
                        )
                        .set_series_opts(
                            tooltip_opts=opts.TooltipOpts(
                                formatter="{b}: {c} ({d}%)"),
                            label_opts=opts.LabelOpts(
                                position="inside", formatter="{b}\n{c}")
                        )
                    )
                    pie_chart_html = pie.render_embed()
                    question_data["pie_chart_html"] = pie_chart_html
                else:
                    print("没有选项或回答数据，无法创建饼图")
                    pie = None
                # pie_chart_html = pie.render_embed()
                # question_data["pie_chart_html"] = pie_chart_html

            elif question.type == 2:
                answers = Answer.objects.filter(question=question)
                text_answers = [answer.answerertext for answer in answers]
                question_data["text_answers"] = text_answers

            question_statistics.append(question_data)
        print("question_statistics",f"{question_statistics}")
        context = {
            'survey': survey,
            "survey_title": survey.title,
            "completion_rate": f"{completion_rate:.2f}%",
            "questions": question_statistics,
        }

        return render(request, "survey_detail.html", context)

    except Survey.DoesNotExist:
        return render(request, "error.html", {"message": "Survey not found"})

from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter


def generate_pdf_from_statistics(survey, statistics, completion_rate):
    """Helper function: Write statistics data to PDF"""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont('SimSun', 12)
    pdf.drawString(50, 750, "{} Survey Statistics".format(survey.title))
    pdf.drawString(50, 730, "Completion Rate: {}".format(completion_rate))
    y_position = 710

    for question in statistics:
        pdf.drawString(50, y_position, f"Question: {question['question_text']}")
        y_position -= 20

        if "options" in question:
            pdf.drawString(60, y_position, "Options:")
            y_position -= 15
            for option in question["options"]:
                pdf.drawString(80, y_position, f"{option['option_text']}: {option['count']}")
                y_position -= 15

        if "text_answers" in question:
            pdf.drawString(60, y_position, "Text Answers:")
            y_position -= 15
            for answer in question["text_answers"]:
                pdf.drawString(80, y_position, answer)
                y_position -= 15

        y_position -= 10  # spacing

        # If exceeding page height, create new page
        if y_position < 50:
            pdf.showPage()
            y_position = 750

    pdf.save()
    buffer.seek(0)
    return buffer

def statistics_pdf(request, survey_id):
    try:
        survey = Survey.objects.get(pk=survey_id)
        questions = Question.objects.filter(survey=survey)
        question_statistics = []
        total_users = User.objects.all().count()
        completed_users = Response.objects.filter(survey=survey).count()
        completion_rate = (completed_users / total_users *100) if total_users > 0 else 0
        for question in questions:
            question_data = {
                "question_text": question.question_text,
            }

            if question.type in [0, 1]:  
                options = Option.objects.filter(question=question)
                option_data = [
                    {"option_text": option.optiontext, "count": Answer.objects.filter(question=question, selectedoption=option).count()}
                    for option in options
                ]
                question_data["options"] = option_data

            elif question.type == 2: 
                answers = Answer.objects.filter(question=question)
                text_answers = [answer.answerertext for answer in answers]
                question_data["text_answers"] = text_answers

            question_statistics.append(question_data)

       
        pdf_buffer = generate_pdf_from_statistics(survey,question_statistics,completion_rate)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{survey.title}_statistics.pdf"'
        return response

    except Survey.DoesNotExist:
        return HttpResponse("Survey does not exist", status=404)


