from celery import task

from tutor.models import Tutor
from matchmaker.models import RequestForTutor, RequestSMS


@task
def send_tutor_request_smses(tutor_pks, request_pks, sms_template_source):
    # TODO
    pass
