from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Enrollment
from payments.models import Transaction
from django.contrib.auth.decorators import login_required

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    queryset = Course.objects.filter(is_published=True)

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    slug_field = 'slug'
