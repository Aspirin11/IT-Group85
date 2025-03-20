from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    name = models.CharField(verbose_name="user", max_length=16, unique=True)
    password = models.CharField(verbose_name="password", max_length=128)
    email = models.EmailField(verbose_name="email", max_length=64)
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):

        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Survey(models.Model):
    STATUS_CHOICES = [
        (0, 'Published'),
        (1, 'Ended')
    ]
    title = models.CharField(verbose_name="Title", max_length=128)
    description = models.TextField(verbose_name="Description", blank=True)
    createby = models.ForeignKey(User, verbose_name="Creator", on_delete=models.CASCADE)
    dateceated = models.DateTimeField(verbose_name="Creation Time", auto_now_add=True)
    startdate = models.DateTimeField(verbose_name="Start Time", blank=True, null=True)
    enddate = models.DateTimeField(verbose_name="End Time", blank=True, null=True)
    status = models.IntegerField(verbose_name="Status", choices=STATUS_CHOICES, default=0)
    participationcount = models.IntegerField(verbose_name="Participation Count", default=0)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "问卷"
        verbose_name_plural = verbose_name

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        (0, 'Single Choice'),
        (1, 'Multiple Choice'), 
        (2, 'Text Question'),
    ]
    survey = models.ForeignKey(Survey, verbose_name="Survey", on_delete=models.CASCADE)
    question_text = models.CharField(verbose_name="Question Content", max_length=256)
    type = models.IntegerField(verbose_name="Question Type", choices=QUESTION_TYPE_CHOICES, default=0)
    order = models.IntegerField(verbose_name="Option Order", default=0)
    isrequired = models.IntegerField(verbose_name="Required", default=0)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "问题"
        verbose_name_plural = verbose_name

class Response(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, null=True, blank=True)
    survey = models.ForeignKey(Survey, verbose_name="Survey", on_delete=models.CASCADE)
    datesubmitted = models.DateTimeField(verbose_name="Submission Time", auto_now_add=True)

    def __str__(self):
        return self.user.name if self.user else "Anonymous"

    class Meta:
        verbose_name = "用户提交"
        verbose_name_plural = verbose_name


class Option(models.Model):
    optiontext = models.CharField(verbose_name="选项内容", max_length=100, blank=True, null=True)
    question = models.ForeignKey(Question, verbose_name="所属问题", on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name="选项序号", default=0)
    def __str__(self):
        return self.optiontext
    class Meta:
        verbose_name = "选项"
        verbose_name_plural = verbose_name

class Answer(models.Model):
    answerertext = models.TextField(verbose_name="答案内容", blank=True, null=True)
    question = models.ForeignKey(Question, verbose_name="所属问题", on_delete=models.CASCADE)
    response = models.ForeignKey(Response, verbose_name="所属用户提交", on_delete=models.CASCADE, blank=True, null=True)
    selectedoption = models.ForeignKey(Option, verbose_name="所属选项", on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.answerertext
    class Meta:
        verbose_name = "回答"
        verbose_name_plural = verbose_name