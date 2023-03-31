from apps.main.models import Comment
from django import forms

class NewCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Write comment'}), required=True)
    
    class Meta:
        model = Comment
        fields = ("text",)