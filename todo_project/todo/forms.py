from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter a task...',
                'class': 'flex-1 px-4 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-indigo-400 focus:outline-none'
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'px-4 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-indigo-400 focus:outline-none'
            })
        }
