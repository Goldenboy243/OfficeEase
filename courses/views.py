from django.shortcuts import render
from .models import Module

def word_course(request):
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft Word").prefetch_related('lessons')
    return render(request, 'courses/word.html', {'modules': modules})

def excel_course(request):
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft Excel").prefetch_related('lessons')
    return render(request, 'courses/excel.html', {'modules': modules})

def powerpoint_course(request):
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft PowerPoint").prefetch_related('lessons')
    return render(request, 'courses/powerpoint.html', {'modules': modules})
