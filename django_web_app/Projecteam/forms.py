from django import forms
from django.forms import ClearableFileInput
from django.contrib.auth.models import User

class TeamCreations(forms.Form):
    name=forms.CharField(max_length=30)
    title=forms.CharField(max_length=20)
    res=User.objects.all()
    choose=[]
    for i in res:
        choose.append((str(i.username),str(i.username)))
    choose=tuple(choose)
    file=forms.FileField(required=False,widget=ClearableFileInput(attrs={'multiple': True}))
    status=forms.BooleanField(required=False)

