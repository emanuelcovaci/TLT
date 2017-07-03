from django import forms
from tinymce.widgets import AdminTinyMCE
from .models import Activity
from utility import clean_file


class ActivityCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    date = forms.SplitDateTimeField()
    show_files = True
    class Meta:
        model = Activity
        fields = ('name', 'file', 'date',)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(ActivityCreationFormAdmin, self).save(commit=False)
        uploaded_file.author = self.current_user
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        if commit:
            uploaded_file.save()
        return uploaded_file


class ActivityChangeFormAdmin(forms.ModelForm):
    show_files = True
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}), label='')
    date = forms.SplitDateTimeField()

    class Meta:
        model = Activity
        fields = ('name', 'file', 'author')

    def __init__(self, *args, **kwargs):
        initial = {
            'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(ActivityChangeFormAdmin, self).__init__(*args, **kwargs)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(ActivityChangeFormAdmin, self).save(commit=False)
        uploaded_file.text = self.cleaned_data['text']
        uploaded_file.date = self.cleaned_data['date']
        if commit:
            uploaded_file.save()
        return uploaded_file
