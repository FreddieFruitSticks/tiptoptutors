from collections import OrderedDict

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from models import Document


class RelatedDocumentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RelatedDocumentsForm, self).__init__(*args, **kwargs)
        # NOTE: This adds a FileField for each model foreign key to Document.
        # The FileField is called '%(fieldname)s_file' where `fieldname` is
        # the name of the foreign key field.
        # It also hides the corresponding Document ModelChoiceField.
        # This means you can only create a new Document using this form,
        # not select an existing Document.
        self.document_fields = []
        ordered_fields = self.fields.items()
        for field in self.Meta.model._meta.fields:
            # skip the field if it's not included in the form
            if field.name not in self.fields:
                continue
            # skip the field if it's not a ForeignKey to Document
            if not field.get_internal_type() == "ForeignKey":
                continue
            if field.rel.to is not Document:
                continue
            name = field.name
            self.document_fields.append(name)
            choice_field = self.fields[name]
            choice_field.widget = forms.HiddenInput(
                attrs=choice_field.widget.attrs)
            index = ordered_fields.index((name, choice_field))
            ordered_fields.insert(index, ('%s_file' % name, forms.FileField(
                required=choice_field.required,
                label=choice_field.label,
                help_text=choice_field.help_text,
                widget=forms.FileInput
            )))
            choice_field.required = False

        self.fields = OrderedDict(ordered_fields)

    def save(self, commit=True):
        for field in self.document_fields:
            document = self.cleaned_data.get(field, None)
            f = self.cleaned_data.get('%s_file' % field, None)
            if document is None:
                if f is None:
                    continue
                document = Document.create_from_file(f)
                self.cleaned_data[field] = document
                setattr(self.instance, field, document)
            else:
                if f is None:
                    document.delete()
                    self.cleaned_data[field] = None
                    setattr(self.instance, field, None)
                else:
                    document.set_file(f)
                    document.save()
        return super(RelatedDocumentsForm, self).save(commit)


class TutorSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(TutorSignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
