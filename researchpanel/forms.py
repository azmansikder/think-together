from django import forms
from .models import ResearchPost


class ResearchPostForm(forms.ModelForm):
    class Meta:
        model = ResearchPost
        fields = ('title', 'abstract', 'content', 'field', 'tags', 'status', 'attachment')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Research Title'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief abstract...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Full research content...'}),
            'field': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AI, Physics, Medicine'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'tag1, tag2, tag3'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }
