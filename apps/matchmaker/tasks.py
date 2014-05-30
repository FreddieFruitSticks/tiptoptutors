from django.template import Template, Context

from celery import task

from sms.api import send_smses
from sms.utils import convert_to_international_format
from matchmaker.models import RequestForTutor, RequestSMS, TutorProxy


@task()
def send_tutor_request_smses(tutor_pks, request_pks, sms_template_source):
    template = Template(sms_template_source)
    # send sms to each tutor individually
    for tutor_pk, request_pk_list in zip(tutor_pks, request_pks):
        requests = RequestForTutor.objects.filter(pk__in=request_pk_list) \
                                          .select_related('subject') \
                                          .order_by('subject__name')
        message = template.render(Context({
            'objects': requests,
            'level': requests[0].pupil.level_of_study,
        }))
        tutor = TutorProxy.objects.get(pk=tutor_pk)
        msisdn = convert_to_international_format(tutor.mobile, '27')
        sms_object, = send_smses('Clickatell', [msisdn], message, True)
        # recreate the SMS object so that it is of type RequestSMS
        sms_object = RequestSMS(id=sms_object.id,
                                mobile_number=sms_object.mobile_number,
                                delivery_status=sms_object.delivery_status,
                                created=sms_object.created,
                                message_id=sms_object.message_id,
                                tutor=tutor)
        sms_object.save()
        sms_object.requests.add(*requests)
