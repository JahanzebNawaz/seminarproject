# from django.contrib.auth import forms
# from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import fields

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