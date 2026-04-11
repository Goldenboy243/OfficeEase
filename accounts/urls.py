from django.contrib import admin
from django.urls import path, include
from . import views # Only if your views are in this folder

urlpatterns = [
    path('admin/', admin.site.urls),  

    path('about-us/', views.about_us, name='about_us'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('login/', views.auth, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('check-email/', views.check_email, name='check_email'),
    path('word/', views.word_course, name='word_course'),
    path('excel/', views.excel_course, name='excel_course'),
    path('powerpoint/', views.powerpoint_course, name='powerpoint_course'),

    path('', views.home, name='home'),
]