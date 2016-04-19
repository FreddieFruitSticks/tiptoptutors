from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email),)

        user.set_password(self.cleaned_data["password"])
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)

        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomAuthUser(AbstractBaseUser, PermissionsMixin):
    # pass
    objects = UserManager()

    username = models.CharField(_('username'), max_length=50, blank=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Deselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # db_table = 'auth_user'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # def __unicode__(self):
    #     return self.email
    #
    # def has_perm(self, perm, obj=None):
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     return True
    #
    # @property
    # def is_staff(self):
    #     return self.is_admin
