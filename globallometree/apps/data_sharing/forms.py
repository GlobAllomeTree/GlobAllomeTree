
from django import forms
from .models import DataLicense, Dataset


class LicenseChoiceForm(forms.Form):
    #Interesting - http://opendefinition.org/licenses/
    LICENSE_CHOICES = (
        ('new', 'Create a new custom license'),
        ('existing', 'Use a custom license that you already created'),
        ('cc0', 'Open Data - CC0 - Creative Commons CCZero'),
        )

    choose_license = forms.ChoiceField(choices=LICENSE_CHOICES)


class DataLicenseForm(forms.ModelForm):
    """
    A form that lets a user create a new dataset, and choose a license
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(DataLicenseForm, self).__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, commit=True): 
        model = super(DataLicenseForm, self).save(commit=False)
        model.User = self.user
        if(commit):
            model.save()
        return model

    class Meta:
        model = DataLicense
        exclude = ('User',)


class ExistingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ExistingForm, self).__init__(*args, **kwargs)
        self.fields["license"].queryset = DataLicense.objects.filter(User=user)

    license = forms.ModelChoiceField(queryset=DataLicense.objects.all(), empty_label=None)


class DatasetUploadForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DatasetUploadForm, self).__init__(*args, **kwargs)
        self.fields["License"].queryset = DataLicense.objects.filter(User=user)

    class Meta:
        model = Dataset
        exclude = ('User',)


