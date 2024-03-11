from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
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
            return render(request,'account/register_done.html',
                          {'user': user})
    else:
        form = UserRegistrationForm()
    
    return render(request,'account/register.html',
                          {'form': form})
    
    
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
