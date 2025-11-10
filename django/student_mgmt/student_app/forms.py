# student_app/forms.py

from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    """Form for adding and updating student records."""
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'roll_number', 'grade', 'major']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    """A simple login form. We use this to demonstrate sessions."""
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))