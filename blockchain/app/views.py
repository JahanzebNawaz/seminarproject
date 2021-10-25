from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views import View
from .forms import SignUpForm, UserProfileForm
from django.contrib.auth.models import User, auth



class Index(View):
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)



class SignUp(View):
    # base instead of signup. singup is included in base with if condition.
    template_name = 'website/base.html'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        user_form = self.form_class()
        context = {
            'user_form': user_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {
            'user_form': form
        }
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        return render(request, self.template_name, context)



class UserLogin(View):
    template_name = 'website/base.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
                auth.login(request, user)
                messages.success(request, f"You are now logged in as {email}.")
                return HttpResponseRedirect('/')
        messages.error(request, 'Authentication Error! make sure you have entered correct credentials.')
        return render(request, self.template_name, self.context)



class UserLogout(View):

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.info(request, 'You have Successfully logout!')
        return HttpResponseRedirect('/')

    

def get_user_id(request):
    return request.user.id


def dashboard(request):
    template_name = 'website/dashboard.html'
    context = {}
    return redirect('website:profile')
    # return render(request, template_name, context)


def profile(request, pk=None):
    template_name = 'website/profile.html'
    context = {
        'form': UserProfileForm,
    }

    if request.GET:
        pk = get_user_id(request)
        user = User.objects.get(pk=pk)
        context['user'] = user
    
    return render(request, template_name, context)