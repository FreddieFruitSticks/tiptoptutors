from django import forms

from models import Document


class RelatedDocumentsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RelatedDocumentsForm, self).__init__(*args, **kwargs)
        self.document_fields = []
        for field in self.Meta.model._meta.fields:
            if not field.get_internal_type() == "ForeignKey":
                continue
            if not field.rel.to is Document:
                continue
            name = field.name
            self.document_fields.append(name)
            file_field = self.fields[name]
            file_field.widget = forms.HiddenInput(attrs=file_field.widget.attrs)
            index = self.fields.keyOrder.index(name)
            self.fields.insert(index, '%s_file' % name, forms.FileField(
                required=file_field.required,
                label=file_field.label,
                help_text=file_field.help_text,
                widget=forms.FileInput
            ))
            file_field.required = False

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
