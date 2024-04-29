from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from users.forms import UserCreateForm, UserUpdateForm
from users.models import CustomUser
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages


class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            'form':create_form
        }
        return render(request, 'users/register.html', context=context)
    
    def post(self, request):
        create_forms = UserCreateForm(data=request.POST)

        if create_forms.is_valid():
            create_forms.save()
            return redirect('users:login')
        else:
            context = {
                'form':create_forms
            }
            return render(request, 'users/register.html', context)
        

class LoginView(View):
    def get(self, request):

        login_form = AuthenticationForm()
        context = {
            'login_form':login_form
        }
        return render(request, 'users/login.html', context)
    

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'You successfully logged in.')
            context = {
                'login_form':login_form
            }
            return redirect('books:list')
        else:
            context = {
                'login_form':login_form
            }
            return render(request, 'users/login.html', context=context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profiles.html', {'user':request.user})
    
    

class LogOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request) 
        messages.info(request, 'You successfully logged out.')
        return redirect('main')


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)
        context = {
            'update_form':user_update_form
        }
        return render(request, 'users/profile-edit.html', context=context)
    
    def post(self, request):
        user_update_form = UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES,
        )

        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request,"You have successfully updated profile.")
            return redirect('users:profile')
        
        context = {
            'update_form':user_update_form
        }
        return render(request, 'users/profile-edit.html', context=context)