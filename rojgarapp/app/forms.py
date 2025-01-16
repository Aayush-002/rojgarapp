from django import forms
from .models import PersonalDetails

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = '__all__'  # Include all fields from the model

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'photo_pp': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'citizenship_photo_front': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'citizenship_photo_back': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'cv_resume': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }
