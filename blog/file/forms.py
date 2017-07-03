from django import forms
from models import Post
from activity.utility import clean_file
from django.forms import modelformset_factory

class PostCreationFormAdmin(forms.ModelForm):
    show_files = True
    class Meta:
        model = Post
        fields = ('name', 'file',)

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(PostCreationFormAdmin, self).save(commit=False)
        if commit:
            uploaded_file.save()
        return uploaded_file


class PostChangeFormAdmin(forms.ModelForm):
    show_files = True
    class Meta:
        model = Post
        fields = ('name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

PostFormSet = modelformset_factory(Post, form=PostCreationFormAdmin)