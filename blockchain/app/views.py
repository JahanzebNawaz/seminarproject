from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views import View
from .forms import SignUpForm, UserProfileForm, UserKycForm, ProposalForm, CustomerForm
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from .models import Customer, UserKyc, Tutorials, Currencies, WatchList

User = get_user_model()


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

def about(request):
    template_name = 'website/about.html'
    return render(request, template_name)

def contact(request):
    template_name = 'website/contact.html'
    return render(request, template_name)


class BlogsView(View):
    template_name = 'website/blogs.html'
    context = {}

    def get(self, request, *args, **kwargs):
        tutorial = Tutorials.objects.all().order_by('-pk')
        tutorial_last = Tutorials.objects.last()
        self.context['tutorials'] = tutorial
        self.context['tutorial_last'] = tutorial_last
        return render(request, self.template_name, self.context)




def blog_detail(request, pk=None):
    template_name = 'website/blog_detail.html'
    tutorial = Tutorials.objects.get(pk=pk)
    tutorials = Tutorials.objects.all()

    context = {
        'tutorial': tutorial,
        'tutorials': tutorials
    }
    return render(request, template_name, context)


def profile(request, pk=None):
    template_name = 'website/profile.html'
    try:
        instance = get_user_id(request)
        user = get_object_or_404(User, pk=instance)
        user_data = model_to_dict(user)
    except Exception as e:
        messages.info(request, f'Error: {str(e)}')
        return redirect('website:index')

    form = CustomerForm(initial=user_data)
    context = {
        'form': form,
    }

    if request.GET:
        pk = get_user_id(request)
        user = User.objects.get(pk=pk)
        context['user'] = user

    if request.POST:
        pk = get_user_id(request)
        user = User.objects.get(pk=pk)
        form = CustomerForm(request.POST, instance=user)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.is_active = True
            # obj.is_superuser = user_data['is_superuser']
            # obj.is_staff = user_data['is_staff']
            obj.save()
            messages.success(request, 'Successfully details updated!')
            return redirect('website:profile')
    return render(request, template_name, context)


class AccountView(View):
    # base instead of signup. singup is included in base with if condition.
    template_name = 'website/account.html'
    form_class = UserProfileForm

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.id)
        form = self.form_class(initial=model_to_dict(user))
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        form = self.form_class(request.POST, request.FILES)
        form.instance.user = request.user
        context = {
            'form': form
        }
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            messages.success(request, 'Successfully submitted!')
            return redirect('website:proposal')
        messages.error(request, f'{form.errors}')
        return render(request, self.template_name, context)


class ProfileView(View):
    # base instead of signup. singup is included in base with if condition.
    template_name = 'website/profile.html'
    form_class = CustomerForm

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.id)
        customer = Customer.objects.filter(user=user).last()
        form = self.form_class(initial=model_to_dict(customer))
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        form = self.form_class(request.POST, request.FILES)
        form.instance.user = request.user
        context = {
            'form': form
        }
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            messages.success(request, 'Successfully submitted!')
            return redirect('website:proposal')
        messages.error(request, f'{form.errors}')
        return render(request, self.template_name, context)


# def userkyc(request, pk=None):
#     template_name = 'website/kycdocs.html'
#     try:
#         instance = get_user_id(request)
#         user = get_object_or_404(User, pk=instance)
#         # user_data = model_to_dict(user)
#         kyc = UserKyc.objects.filter(user=user).last()
        

#     except Exception as e:
#         messages.info(request, f'Error: {str(e)}')
#         return redirect('website:index')

#     form = UserKycForm()
#     context = {
#         'form': form,
#     }

#     if kyc:
#         context['kyc'] = kyc

#     if request.GET:
#         pk = get_user_id(request)
#         user = User.objects.get(pk=pk)
        
#         context['user'] = user
    
#     if request.POST:
#         pk = get_user_id(request)
#         user = User.objects.get(pk=pk)
#         print(user)
#         print(request.POST.get('kyc_documents'))

#         form_data = UserKycForm(request.POST, request.FILES, instance=user)
#         if form_data.is_valid():
#             # obj = form.save(commit=False)
#             form_data.save()
#             messages.success(request, 'Successfully KYC Documents Submmited!')
#             return redirect('website:userkyc')
#         print(form.errors)
#     return render(request, template_name, context)



class UserKycView(View):
    # base instead of signup. singup is included in base with if condition.
    template_name = 'website/kycdocs.html'
    form_class = UserKycForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        kyc_data = UserKyc.objects.filter(user=request.user.id).last()
        print(kyc_data)
        context = {
            'form': form,
            'kyc': kyc_data,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        form = self.form_class(request.POST, request.FILES)
        form.instance.user = request.user
        context = {
            'form': form
        }
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            messages.success(request, 'Successfully submitted!')
            return redirect('website:userkyc')
        messages.error(request, f'{form.errors}')
        return render(request, self.template_name, context)


class ProposalView(View):
    # base instead of signup. singup is included in base with if condition.
    template_name = 'website/base.html'
    form_class = ProposalForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        form = self.form_class(request.POST, request.FILES)
        form.instance.user = request.user
        context = {
            'form': form
        }
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            messages.success(request, 'Successfully submitted!')
            return redirect('website:proposal')
        messages.error(request, f'{form.errors}')
        return render(request, self.template_name, context)



class CurrenciesView(View):
    template_name = 'website/cryptos.html'
    context = {}

    def get(self, request, *args, **kwargs):
        cryptos = Currencies.objects.all()
        self.context['cryptos'] = cryptos
        return render(request, self.template_name, self.context)


def add_to_watch(request, pk):
    
    user = request.user
    currency = Currencies.objects.get(pk=pk)
    obj = WatchList.objects.create(user=user, currency=currency)
    if obj:
        messages.success(request, f'{currency} added to watch list')
    return redirect('website:cryptos')



def watchlist(request, pk=None): 
    template_name = 'website/watchlist.html'   
    user = request.user.id
    queryset = WatchList.objects.filter(user=user)
    context = {
        'watchlist': queryset
    }
    return render(request, template_name, context)

