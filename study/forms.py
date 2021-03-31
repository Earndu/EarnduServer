from django import forms
from study.models import Category

class ContentForm(forms.Form):
    MAX_LENGTH = 60
    BORDER_COLOR = '505050'
    BORDER_RADIUS = 10
    PADDING = 5

    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'style': 'width: %sch; border: 1px solid #%s; border-radius: %spx; padding: %spx;' %(MAX_LENGTH, BORDER_COLOR, BORDER_RADIUS, PADDING)}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style': 'width: %sch; border: 1px solid #%s; border-radius: %spx; padding: %spx;' %(MAX_LENGTH, BORDER_COLOR, BORDER_RADIUS, PADDING)}))
    title = forms.CharField(widget=forms.widgets.TextInput(attrs={'style': 'width: %sch; border: 1px solid #%s; border-radius: %spx; padding: %spx;' %(MAX_LENGTH, BORDER_COLOR, BORDER_RADIUS, PADDING)}))
    category = forms.ChoiceField(choices=[(cat.id, cat.english) for cat in Category.objects.all()])
    type = forms.ChoiceField(choices=((0,'Text'), (1,'Voice'), (2,'Image')))
    content = forms.CharField(widget=forms.widgets.Textarea(
        attrs={'style': 'width: %sch; height: 20ch; border: 1px solid #%s; border-radius: %spx; padding: %spx;' %(int(MAX_LENGTH * 1.05), BORDER_COLOR, BORDER_RADIUS, PADDING)}), required=False)
    level = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={'style': 'width: %sch; border: 1px solid #%s; border-radius: %spx; padding: %spx;' %(MAX_LENGTH, BORDER_COLOR, BORDER_RADIUS, PADDING)}))

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
