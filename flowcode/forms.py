import datetime

from django.forms import ModelForm, Form
from .models import *
from django.forms import FileField
from django import forms


class PyFileForm(ModelForm):
    class Meta:
        model = PyFile
        fields = ['name', 'file', 'color']


class FiForm(Form):
    name = forms.CharField(max_length=255)
    file = forms.FileField()
    color = forms.CharField(max_length=255)


DEMO_CHOICES =(
    ("1", "doughnut"),
    ("2", "line"),
    ("3", "area"),
    ("4", "column"),
    ("5", "pie"),
)


class GraphForm(Form):
    title = forms.CharField(max_length=255)
    json = forms.CharField()
    type = forms.MultipleChoiceField(choices=DEMO_CHOICES)

class VizForm(forms.ModelForm):
    class Meta:
        model = VizQuery
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class CandleForm(ModelForm):
    class Meta:
        model = Candle
        fields = ['ticker']

