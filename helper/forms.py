from django import forms 
from .models import Request, Comment

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'body', 'location', 'profession', 'request_type']
        
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['text','is_special']

