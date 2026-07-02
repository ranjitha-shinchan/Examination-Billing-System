# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_choice, name='exam_choice'),
    path('theory-step1/', views.theory_examination_step1, name='theory_examination_step1'),
    path('theory-step2/', views.theory_examination_step2, name='theory_examination_step2'),
    path('theory-success/', views.theory_examination_success, name='theory_examination_success'),
    path('practical-exam/step1/', views.practical_examination_step1, name='practical_examination_step1'),
    path('practical-exam/step2/', views.practical_examination_step2, name='practical_examination_step2'),
    path('practical-exam/success/', views.practical_examination_success, name='practical_examination_success'),
    path('records/', views.view_records_choice, name='view_records_choice'),
    path('records/theory/', views.view_theory_records, name='view_theory_records'),
    path('records/practical/', views.view_practical_records, name='view_practical_records'),
]
