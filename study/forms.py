from django import forms
from study.models import Category

class ContentForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    title = forms.CharField()
    category = forms.ChoiceField(choices=[(cat.id, cat.english) for cat in Category.objects.all()])
    type = forms.ChoiceField(choices=((0,'Text'), (1,'Voice'), (2,'Image')))
    content = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows': 30, 'cols': 100}), required=False)
    level = forms.IntegerField()