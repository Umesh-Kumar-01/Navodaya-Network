from django import forms 
from .models import Request, Comment

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'body', 'location', 'profession', 'request_type']
        
class CommentForm(forms.ModelForm):
    # Additional fields for the modal
    class Meta:
        model = Comment
        fields = ['text', 'is_special', 'mobile_number', 'email']

    def save(self, commit=True):
        instance = super().save(commit=False)
        mobile_number = self.cleaned_data.get('mobile_number', None)
        email = self.cleaned_data.get('email', None)
        instance.is_special = mobile_number is not None or email is not None
        if commit:
            instance.save()
        return instance
