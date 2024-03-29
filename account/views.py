from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm,UserEditForm, ProfileEditForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Profile,Contact
from actions.utils import create_action
from actions.models import Action
# Create your views here.


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')\
        .prefetch_related('target')[:10]
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                  'actions': actions})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(
                form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            create_action(user,'has created an account')
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
        
@login_required
def user_list(request):
     users = User.objects.filter(is_active=True)
     return render(request,
                   'account/user/list.html',
                   {'section':'people',
                    'users':users}) 
     
     
@login_required
def user_detail(request,username):
    user = get_object_or_404(User, username=username,
                             is_active=True)
    return render(request,
                    'account/user/detail.html',
                    {'section': 'people',
                    'user': user})
    

@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id = user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                create_action(request.user,'is following',user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})