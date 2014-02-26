from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from student.forms import StudentForm
from django.http import HttpResponseRedirect
from student.models import Student


class StudentView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "student/student.html"
    success_url = "/student/success/"

    def form_valid(self, form):
        super(StudentView,self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class StudentSuccessView(TemplateView):
    template_name = "student/student-complete.html"