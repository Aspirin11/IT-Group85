"""
URL configuration for Data project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from datapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',include('pp.urls')),
    path('',views.login),
    path('loginout/',views.logout),
    path('login/',views.login),
    path('res/',views.res),
    path('survey_analysis/', views.survey_analysis, name='survey_analysis'),
    path('surveys/<int:survey_id>/', views.survey_statistics, name='survey_detail'),
    path('change_password/', views.change_password),
    path('create_survey/', views.create_survey, name='create_survey'),
    path("surveys/", views.survey_list, name="survey_list"),
    path("surveys/<int:survey_id>/delete/", views.delete_survey, name="delete_survey"),
    path("surveys/<int:survey_id>/edit/", views.edit_survey, name="edit_survey"),
    path("surveys/<int:survey_id>/", views.survey_statistics, name="survey_detail"),
    path("fill_survey/<int:survey_id>/", views.fill_survey, name="fill_survey"),
    path("survey_list/", views.surveys, name="surveys"),
    # path("statistics/<int:survey_id>/", views.survey_statistics, name="statistics"),
    path('statistics_pdf/<int:survey_id>/', views.statistics_pdf, name='statistics_pdf'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
