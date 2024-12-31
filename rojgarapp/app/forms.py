from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class UserDetailsForm(forms.Form):
    # Personal Details
    first_name = forms.CharField(label=_('First Name'), max_length=100, required=True)
    middle_name = forms.CharField(label=_('Middle Name'), max_length=100, required=False)
    last_name = forms.CharField(label=_('Last Name'), max_length=100, required=True)
    dob = forms.DateField(label=_('Date of Birth'), required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    mobile_number = forms.CharField(
        label=_('Mobile Number'),
        max_length=10,
        required=True,
        validators=[RegexValidator(r'^\d{10}$', _('Enter a valid mobile number'))]
    )
    contact_number = forms.CharField(
        label=_('Contact Number'),
        max_length=10,
        required=False,
        validators=[RegexValidator(r'^\d{10}$', _('Enter a valid contact number'))]
    )
    email_address = forms.EmailField(label=_('Email Address'), required=False)
    national_id_number = forms.CharField(label=_('National ID Number'), max_length=50, required=False)
    gender = forms.ChoiceField(
        label=_('Gender'),
        choices=[('male', _('Male')), ('female', _('Female')), ('others', _('Others'))],
        required=True
    )
    citizenship_number = forms.CharField(label=_('Citizenship Number'), max_length=50, required=True)
    citizenship_issued_date = forms.DateField(
        label=_('Citizenship Issued Date'), required=True, widget=forms.DateInput(attrs={'type': 'date'})
    )
    citizenship_issued_district = forms.CharField(label=_('Citizenship Issued District'), max_length=100, required=True)

    # Parent Details
    fathers_name = forms.CharField(label=_('Father’s Name'), max_length=100, required=True)
    mothers_name = forms.CharField(label=_('Mother’s Name'), max_length=100, required=True)
    spouse_name = forms.CharField(label=_('Wife/Husband’s Name'), max_length=100, required=False)

    # Permanent Address
    permanent_province = forms.CharField(label=_('Province'), max_length=100, required=True)
    permanent_district = forms.CharField(label=_('District'), max_length=100, required=True)
    permanent_municipality_name = forms.CharField(label=_('Municipality Name'), max_length=100, required=True)
    permanent_ward_no = forms.IntegerField(label=_('Ward No'), required=True)
    permanent_tole_name = forms.CharField(label=_('Tole Name'), max_length=100, required=True)

    # Current Address
    current_province = forms.CharField(label=_('Province'), max_length=100, required=True)
    current_district = forms.CharField(label=_('District'), max_length=100, required=True)
    current_municipality_name = forms.CharField(label=_('Municipality Name'), max_length=100, required=True)
    current_ward_no = forms.IntegerField(label=_('Ward No'), required=True)
    current_tole_name = forms.CharField(label=_('Tole Name'), max_length=100, required=True)

    # Education Background
    education_background = forms.ChoiceField(
        label=_('Education Background'),
        choices=[
            ('slc_see', _('SLC/SEE')),
            ('plus_two', _('+2')),
            ('bachelor', _('Bachelor')),
            ('masters', _('Masters')),
            ('diploma', _('Diploma'))
        ],
        required=True
    )
    professional_skill = forms.CharField(label=_('Professional Skill'), max_length=200, required=False)

    # File Uploads
    photo = forms.ImageField(label=_('Photo (PP Size)'), required=True)
    citizenship_photo_front = forms.ImageField(label=_('Citizenship Photo (Front)'), required=True)
    citizenship_photo_back = forms.ImageField(label=_('Citizenship Photo (Back)'), required=True)
    cv_resume = forms.FileField(label=_('CV/Resume'), required=True)
