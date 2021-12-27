from django import forms
from .models import Author

class EditProfile(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['name','phone','address','profile_pic']