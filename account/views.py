from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm,UserEditForm, ProfileEditForm
from .models import Profile
# Create your views here.


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(
                form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            return render(request,'account/register_done.html',
                          {'user': user})
    else:
        form = UserRegistrationForm()
    
    return render(request,'account/register.html',
                          {'form': form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance = request.user,
                            data = request.POST)
        
        profile_form = ProfileEditForm(instance = request.user.profile,
                                       data = request.POST,
                                       files = request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated seccessfuly')
            return redirect('dashboard')
            
        else:
            messages.error(request,"Error updating your profile")
            
            
            
            
    else:
            user_form = UserEditForm(instance = request.user)
            profile_form = ProfileEditForm(instance = request.user.profile)
            
    return render(request,'account/edit.html',{'user_form':user_form,
                                                   'profile_form':profile_form})
        
    
'''def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')

            else:
                return HttpResponse('Inavlid Login')
    else:
            form = LoginForm()

    return render(request, 'account/login.html', {'form': form}) '''
