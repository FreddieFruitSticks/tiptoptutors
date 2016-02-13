from common.forms import RelatedDocumentsForm
from tutor.models import Tutor


class TutorDetailsForm(RelatedDocumentsForm):
    class Meta:
        model = Tutor
        exclude = ('lesson', 'comment', 'status', 'user', 'name', 'surname', 'email')
