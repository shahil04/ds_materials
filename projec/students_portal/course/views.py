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


@login_required
def enroll_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    # If already enrolled and paid, redirect to course panel
    if Enrollment.objects.filter(user=request.user, course=course, paid=True).exists():
        return redirect('student_course_panel', slug=course.slug)

    if course.price == 0:
        # free course -> create enrollment
        enrollment = Enrollment.objects.create(user=request.user, course=course, paid=True)
        return redirect('student_course_panel', slug=course.slug)

    # Paid course -> create Transaction & start payment flow (see payments section)
    return redirect('payments:create_order', course_id=course.id)
