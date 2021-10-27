# from django.contrib.auth import forms
# from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import fields
from .models import Customer, UserKyc, Proposals, Wallet
from datetime import datetime


User = get_user_model()



class SignUpForm(UserCreationForm):
    #profile_year        = blaaa blaa blaaa irrelevant.. You have your own stuff here don't worry about it
    # here is the important part.. add a class Meta-
    # first_name = forms.CharField(max_length=30, required=False)
    # last_name = forms.CharField(max_length=30, required=False)
    # date_of_birth = forms.DateField(required=False)

    class Meta:
        model = User #this is the "YourCustomUser" that you imported at the top of the file  
        fields = ('username','email', 'password1', 'password2',) #etc etc, other fields you want displayed on the form)



class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['date_joined', 'password']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        date_of_birth = cleaned_data.get('date_of_birth')
        year = datetime.today().year
        age = year - date_of_birth.year
        if age < 18:
            raise forms.ValidationError(u"Please check your DOB, under 18 restricted!")
        return cleaned_data


class UserKycForm(forms.ModelForm):

    class Meta:
        model = UserKyc
        # fields = '__all__'
        fields = ('kyc_documents',)


class ProposalForm(forms.ModelForm):
    details =  forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":100}))

    class Meta:
        model = Proposals
        fields = '__all__'
        exclude = ['user',]


class WalletForm(forms.ModelForm):

    class Meta:
        model = Wallet
        fields = '__all__'
        exclude = ['user',]