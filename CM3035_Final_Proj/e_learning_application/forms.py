from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
#---for password validation---# 
import re

ROLE_CHOICES = [
    ('Student', 'Student'),
    ('Teacher', 'Teacher'),
]


#---------------form for creating new users------------------#
class UserRegistrationForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Required. 8 Characters minimally. Consisting of at least 1 upper and lower casing letters and digits"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    #---This part is to arrange the order of how the fields are displayed on the page  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #---removing the default help text---#
        self.fields['username'].help_text = None

        #---Rearranging the order of the fields--#
        self.fields = {
            'role': self.fields['role'],
            'username': self.fields['username'],
            'email': self.fields['email'],
            'password': self.fields['password'],
        }


    #-----imposing retrictions/criteria for the password-------#
    def clean_password(self):
        password = self.cleaned_data.get('password')

        #---Validating password requirements---#
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.")

        return password


#----------------form for logging in-------------#
class UserLoginForm(forms.Form):
    role = forms.ChoiceField(label="Login as", choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


#-----form for the courses and courseContent--------#
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['courseTitle', 'courseDescription']


class CourseContentForm(forms.ModelForm):
    class Meta:
        model = CourseContent
        fields = ['contentTitle', 'course', 'file']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedbackText']

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdates
        fields = ['status_content']






