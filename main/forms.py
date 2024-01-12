from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    name = forms.CharField()
    title = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Contact
        fields = ['email', 'name', 'title', 'message', 'phone']

