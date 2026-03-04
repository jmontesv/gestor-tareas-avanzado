from django import forms
from .models import Task, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'assigned_to', 'priority', 'labels', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'assigned_to': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'priority': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'labels': forms.SelectMultiple(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded px-3 py-2'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'nombre_completo', 'bio', 'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }