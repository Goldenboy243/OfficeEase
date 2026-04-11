from django.urls import path
from . import views

urlpatterns = [
    path('word/', views.word_course, name='word_course'),
    path('excel/', views.excel_course, name='excel_course'),
    path('powerpoint/', views.powerpoint_course, name='powerpoint_course'),
]
