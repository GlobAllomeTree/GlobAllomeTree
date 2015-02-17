
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from globallometree.apps.locations.models import Country


class RegistrationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    
    title = forms.CharField(label='Title', max_length=10)
    first_name = forms.CharField(label='First name', max_length=30)
    last_name  = forms.CharField(label='Last name', max_length=30)
    
    username  = forms.RegexField(label="Username", max_length=30, regex=r'^[\w.@+-]+$',
            help_text = "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
            error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
    
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput,
            help_text = "Enter the same password as above, for verification.")
    
    address     = forms.CharField(label='Address', max_length=200)

    country     = forms.ModelChoiceField(queryset=Country.objects.all(), 
                                         to_field_name='Common_name')

    subregion   = forms.CharField(label='Subregion', max_length=80, required=False)
    region      = forms.CharField(label='Region', max_length=80, required=False)
    
    privacy = forms.ChoiceField(label='Profile Privacy', 
                                choices=UserProfile.PRIVACY_CHOICES,
                                initial='public')

    email       = forms.EmailField(label="Email")
    education   = forms.ChoiceField(label='Education', 
                                    choices=UserProfile.EDUCATION_CHOICES)

    institution_name      = forms.CharField(label='Name of Institution', max_length=200, required=False)
    institution_address   = forms.CharField(label='Institution Address', max_length=200, required=False)
    institution_phone     = forms.CharField(label='Institution Phone', max_length=60, required=False)
    institution_fax       = forms.CharField(label='Institution Fax', max_length=60, required=False)
    field_subject         = forms.CharField(label='Field Subject', max_length=60)

    data_may_provide      = forms.ChoiceField(label='Data you may provide', choices=UserProfile.DATA_MAY_PROVIDE_CHOICES, required=False)

    accept_terms_software   = forms.BooleanField(label='I accept the Terms and Conditions related to the Fantallometrik Software.')
    accept_terms_databases  = forms.BooleanField(label='I accept the GlobAllomeTree Databases Terms of Use and User Rights.')
    accept_terms_website    = forms.BooleanField(label='I accept the GlobAllomeTree Website Terms and Conditions.')
   
    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("A user with that email already exists.")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        
        if commit:
            user.save()
        return user