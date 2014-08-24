from django.db import models

from common.forms import RelatedDocumentsForm
from tutor.models import Tutor


class TutorForm(RelatedDocumentsForm):

    class Meta:
        model = Tutor
        exclude = ('lesson', 'comment', 'status')
