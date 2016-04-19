from django import forms
from django.contrib.auth import get_user_model
from customuser.forms import CustomUserCreationForm


class UserTutorSignupForm(CustomUserCreationForm):
    # email2 = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print(email)
        # username = self.cleaned_data.get("username")
        # print(username)
        #
        # if email and username and email != username:
        #     print("invalid passwords")
        #     raise forms.ValidationError(
        #         'email mismatch',
        #         code='email_mismatch',
        #     )
        return email

    def save(self, commit=True):
        user = super(UserTutorSignupForm, self).save(commit=False)
        user.email = self.cleaned_data["username"]
        user.set_password(self.cleaned_data['password2'])
        print "password2", self.cleaned_data['password2']
        if commit:
            user.save()
        return user


# class MyPasswordRecoveryForm(PasswordRecoveryForm):
