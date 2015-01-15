
from django.db.models import Q
from django import forms
from .models import DataLicense, Dataset


class LicenseChoiceForm(forms.Form):
    #Interesting - http://opendefinition.org/licenses/
    LICENSE_CHOICES = (
        ('', '-- Create or Select License --'),
        ('new', 'Create a new custom license'),
        ('existing', 'Use a custom license that you already created'),
        ('creative', 'Select a creative commons license'),
        )

    choose_license = forms.ChoiceField(choices=LICENSE_CHOICES)


class DataLicenseForm(forms.ModelForm):
    """
    A form that lets a user create a new dataset, and choose a license
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(DataLicenseForm, self).__init__(*args, **kwargs)
        self.fields['Expires'].widget = forms.RadioSelect()
        self.fields['Permitted_use'].widget = forms.RadioSelect() 

    def save(self, force_insert=False, force_update=False, commit=True): 
        model = super(DataLicenseForm, self).save(commit=False)
        model.User = self.user
        if(commit):
            model.save()
        return model

    class Meta:
        model = DataLicense
        exclude = ('User', 'Restrictive', 'Public_choice', 'License_url')


class ExistingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ExistingForm, self).__init__(*args, **kwargs)
        self.fields["license"].queryset = DataLicense.objects.filter(User=self.user)

    license = forms.ModelChoiceField(queryset=DataLicense.objects.all(), 
                                     empty_label=None, 
                                     required=True,
                                     label='Existing License')


class CreativeForm(forms.Form):

    license = forms.ModelChoiceField(queryset=DataLicense.objects.filter(Public_choice=True), 
                                     empty_label=None, 
                                     required=True,
                                     label='Creative Commons License')



class DatasetUploadForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(DatasetUploadForm, self).__init__(*args, **kwargs)
        self.fields["Data_license"].queryset = DataLicense.objects.filter(
            Q(User=self.user) | Q(Public_choice=True)).order_by('-Public_choice', 'Title')

    def save(self, force_insert=False, force_update=False, commit=True): 
        model = super(DatasetUploadForm, self).save(commit=False)
        model.User = self.user
        #Set is restricted
        if(commit):
            #Validate the data! Party!!!
            model.save()
        return model

    class Meta:
        model = Dataset
        exclude = ('User', 'Imported')


