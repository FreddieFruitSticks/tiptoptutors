from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from password_reset.forms import PasswordRecoveryForm


class UserTutorSignupForm(UserCreationForm):
    # email2 = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print(email)
        username = self.cleaned_data.get("username")
        print(username)

        if email and username and email != username:
            print("invalid passwords")
            raise forms.ValidationError(
                'email mismatch',
                code='email_mismatch',
            )
        return email

    def save(self, commit=True):
        user = super(UserTutorSignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# class MyPasswordRecoveryForm(PasswordRecoveryForm):
