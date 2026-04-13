from django.urls import path
from . import views

urlpatterns = [
    path('word/', views.word_course, name='word_course'),
    path('excel/', views.excel_course, name='excel_course'),
    path('powerpoint/', views.powerpoint_course, name='powerpoint_course'),
    path('structured/<int:course_id>/', views.structured_course, name='structured_course'),
    path('steps/<int:step_id>/complete-theory/', views.complete_theory_step, name='complete_theory_step'),
    path('steps/<int:step_id>/submit-practice/', views.submit_practice_step, name='submit_practice_step'),
]
