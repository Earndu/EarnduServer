from django import forms
from study.models import Category

class ContentForm(forms.Form):
    MAX_LENGTH = 60
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'style': 'width: %sch' %MAX_LENGTH}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width: %sch' %MAX_LENGTH}))
    title = forms.CharField(widget=forms.widgets.TextInput(attrs={'style': 'width: %sch' %MAX_LENGTH}))
    category = forms.ChoiceField(choices=[(cat.id, cat.english) for cat in Category.objects.all()])
    type = forms.ChoiceField(choices=((0,'Text'), (1,'Voice'), (2,'Image')))
    content = forms.CharField(widget=forms.widgets.Textarea(
        attrs={'style': 'width: %sch; height: 20ch;' %(int(MAX_LENGTH*1.05))}), required=False)
    level = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={'style': 'width: %sch' %MAX_LENGTH}))

class ContentFormMobile(forms.Form):
    MAX_LENGTH = 30
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'style': 'width: %sch' %MAX_LENGTH}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width: %sch' %MAX_LENGTH}))
    title = forms.CharField(widget=forms.widgets.TextInput(attrs={'style': 'width: %sch' %MAX_LENGTH}))
    category = forms.ChoiceField(choices=[(cat.id, cat.english) for cat in Category.objects.all()])
    type = forms.ChoiceField(choices=((0,'Text'), (1,'Voice'), (2,'Image')))
    content = forms.CharField(widget=forms.widgets.Textarea(
        attrs={'style': 'width: %sch; height: 20ch;' %(int(MAX_LENGTH*1.05))}), required=False)
    level = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={'style': 'width: %sch' %MAX_LENGTH}))
