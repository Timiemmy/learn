from django.shortcuts import render
from .models import Course
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy


class ManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'

# override the get_queryset() method of the view to retrieve only courses created by the current user.
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.filter)


# This class can be used for views that interact with any model that contains an owner attribute.
class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    # The fields of the model to build the model form of the CreateView and UpdateView views.
    fields = ['subject', 'title', 'slug', 'overview']
    # Used by CreateView, UpdateView, and DeleteView to redirect the user after the form is successfully submitted or the object is deleted.
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    # The template you will use for the CreateView and UpdateView views.
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    # Lists the courses created by the user. It inherits from OwnerCourseMixin and ListView.
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    # Uses a model form to create a new Course object. It uses the fields defined in OwnerCourseMixin to build a model form and also subclasses CreateView
    permission_required = 'courses.add_courses'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    '''Allows the editing of an existing Course object. It uses the fields defined in
OwnerCourseMixin to build a model form and also subclasses UpdateView. It uses the template
defined in OwnerCourseEditMixin.'''
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    # Inherits from OwnerCourseMixin and the generic DeleteView.
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'
