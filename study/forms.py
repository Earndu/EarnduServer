from django import forms
from study.models import Category

class ContentForm(forms.Form):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'style': 'width: 50ch'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width: 50ch'}))
    title = forms.CharField(widget=forms.widgets.TextInput(attrs={'style': 'width: 50ch'}))
    category = forms.ChoiceField(choices=[(cat.id, cat.english) for cat in Category.objects.all()])
    type = forms.ChoiceField(choices=((0,'Text'), (1,'Voice'), (2,'Image')))
    content = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows': 20, 'cols': 50}), required=False)
    level = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={'style': 'width: 50ch'}))