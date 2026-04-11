from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
]
