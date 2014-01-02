from django.views.generic import TemplateView
from django.views.generic.edit import FormView
# from student.forms import StudentForm
from django.http import HttpResponseRedirect
from student.forms import StudentForm


class StudentView(FormView):

    form_class = StudentForm
    template_name = "student/student.html"
    success_url = ('/student-success')

    def form_valid(self, form):
        super(StudentView,self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class StudentSuccessView(TemplateView):
    template_name = "student/student-success.html"
