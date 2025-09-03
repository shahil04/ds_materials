from django.contrib import admin
from .models import Course, Lesson, Enrollment

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','price','is_published','created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]

admin.site.register(Enrollment)
