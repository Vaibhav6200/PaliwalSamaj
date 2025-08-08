from django import forms
from SamajApp.models import Culture
from django_ckeditor_5.widgets import CKEditor5Widget


class CultureCreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Culture
        fields = ('title_en', 'title_hi', 'slug', 'content')  # include translations
        content = CKEditor5Widget(attrs={"class": "django_ckeditor_5", "style": "min-height:600px;"}, config_name='extends')
