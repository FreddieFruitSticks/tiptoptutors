from django.contrib.auth.models import User
from django.db import models
from area.models import Region


class UserProfile(models.Model):
    user = models.OneToOneField(User)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.get_profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
