from django import forms
from .models import Task

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

