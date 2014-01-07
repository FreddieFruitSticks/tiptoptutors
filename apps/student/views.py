from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from student.forms import StudentForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from student.models import Student

class StudentView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "student/student.html"

    def form_valid(self, form):
        super(StudentView,self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("student-success")

class StudentSuccessView(TemplateView):
    template_name = "student/student-success.html"