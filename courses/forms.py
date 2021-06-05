from django import forms
from django.contrib.auth.models import User
from .models import Class, Subject, Lesson



class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        help_texts = {
            'title': 'Class 12',
            'description':'A brief description of the class',
            'image':'You can post a class photo or it can be left blank'
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['creator','slug', 'title', 'classa', 'description', 'image_upload']
        help_texts = {
            'title': 'Title',
            'description':'Put a brief description of the subject',
            'classa':'Choose the class for which you will create the subject',
            'image_upload':'You can put a photo of the subject or it can be left blank'
        }
        labels = {
            'title':'Title of the subject'
        }
        widgets = {'creator': forms.HiddenInput(), 'slug': forms.HiddenInput()}


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson 
        fields = ['slug','title', 'subject', 'video_id', 'position', ]
        help_texts = {
            'title':'Enter the title of the lesson',
            'subject':'Choose the subject for which this lesson belongs',
            'video_id':'Enter the ID of the Youtube video you will upload (<a href="/media/youtube_help.png">where can i find the ID</a>)',
            'position':'Enter the position number or order of instruction '
        }
        widgets = {
            'slug': forms.HiddenInput()
        }