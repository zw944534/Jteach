'''
Created on 2022年2月13日

@author: chu
'''
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from .models import Profile,Product
from django.contrib.auth.decorators import login_required,permission_required
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm,ProductForm
from django.contrib.auth.models import Permission 
import requests
from django.views.generic.edit import UpdateView
from .search_article import search


def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

# class UserPermissionView(UpdateView):
    # model = Profile
    # template_name = 'user_permission.html' # Your template name
    # form_class = UserPermissionsForms
    # initial = {}  # We'll update the form's fields by their initial values
    #
    # def get_initial(self):
    #     """Update the form_class's fields by their initials"""
    #
    #     base_initial = super().get_initial()
    #     # Here we'll check if the user has the permission of 'change_user'
    #     user_has_permission = self.request.user.user_permissions.filter(
    #         codename='change_user'
    #     ).first()
    #     base_initial['change_user'] = True if user_has_permission else False
    #     return base_initial
    #
    # def form_valid(self, form):
    #     """
    #     Here we'll update the user's permission based on the form choice:
    #     If we choose: Yes => Add 'change_user' permission to the user
    #                   No => Remove 'change_user' permission from the user
    #     """
    #     change_user = form.cleaned_data['change_user']
    #     permission = Permission.objects.get(codename='change_user')
    #     if change_user == 'True':
    #         self.request.user.user_permissions.add(permission)
    #         # Use django's messaging framework
    #         # We'll render the results into the template later
    #         messages.success(
    #             self.request,
    #             'Updated: User [{}] Can change user'.format(self.request.user.username)
    #         )
    #     else:
    #         self.request.user.user_permissions.remove(permission)
    #         messages.success(
    #             self.request,
    #             'Updated: User [{}] Cannot change user'.format(self.request.user.username)
    #         )
    #     return super().form_valid(form)
    #
    # def get_success_url(self):
    #     """
    #        Don't forget to add your success URL,
    #        basically use the same url's name as this class view
    #     """
    #     # Note here, we'll access to the URL based on the user pk number
    #     return reverse_lazy('user_permissions', kwargs={'pk': self.request.user.pk})

def permissionDeniedView(request):
    user = request.user;
    return render(request,'users/user_permissions.html',{'user':user})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        print(request.user._wrapped)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def product(request):
    profile = Profile.objects.get(user=request.user);
    productList = profile.product.all();
    if request.method == 'POST':
        productForm = ProductForm(request.POST)
        if productForm.is_valid():
            post = productForm.save(commit=False)
            post.user = profile
            post,created = Product.objects.update_or_create(user=profile,name=post.name,desc=post.desc)
            search(post.name,profile)
            return redirect(to='product-form')
    else:
        productForm = ProductForm(instance = request.user)
    return render(request, 'users/product.html', {'product_form': productForm,'product_list':productList})

@login_required
def productArticle(request):
    profile = Profile.objects.get(user=request.user);
    productList = profile.product.all();
    test = list(productList)
    articleList=[]
    for i in test:
        id = i.id
        name = i.name
        wordCloud = i.wordcloud
        print(wordCloud);
        article = list(i.article.all())
        articleList.append(dict(name=name,article=article,id=id,wordcloud=wordCloud))
    
    return render(request,'users/product_article.html',{'productList':articleList})