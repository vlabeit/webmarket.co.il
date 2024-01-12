from django.contrib.auth import login

from users.models import CustomUser, UserAgent
from django.contrib.auth import views
from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AuthenticationFormNew, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from user_agents import parse
from django.utils import timezone
import requests
import json
from allauth.account.views import EmailAddress


def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip


def get_geolocation_for_ip(ip):
    url = f"http://api.ipstack.com/{ip}?access_key=54d8e1636e724841ed6f7c16656b6db9"

    headers = {}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    #print(f"Status code1: {r.status_code}")

    # Store API response in a variable.
    response_dict = r.json()
    data = json.dumps(response_dict, indent=2)
    city = response_dict['city']
    country = response_dict['country_name']
    if city and country:
        return f"{city}, {country}"
    else:
        return "local"


def get_usera(request):
    ua_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(ua_string)
    str(user_agent)  # returns "iPhone / iOS 5.1 / Mobile Safari 5.1"
    return user_agent


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            newreg = form.save(commit=False)
            newreg.ip_address = get_ip(request)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            newreg.user = authenticate(
                username=username, password=raw_password)
            newreg.save()
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'full_name': CustomUser.get_full_name(request.user),
    }

    return render(request, 'users/profile.html', context)


class UpdatePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = 'password-change/password-changed'
    template_name = 'users/password-change.html'


@login_required
def passwordchanged(request):
    return render(request, 'users/password-changed.html')


@login_required
def verification_sent(request):
    return render(request, 'users/verification-sent.html')


@login_required
def usersettings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    last_logins = UserAgent.objects.filter(
        user_id=request.user).order_by('-time')
    #emails = EmailAddress.objects.get(user_id=request.user.id)

    context = {
        'last_logins': last_logins,
        'u_form': u_form,
        'p_form': p_form,
        # 'emails': emails,
    }

    return render(request, 'users/usersettings-base.html', context)


class LoginNew(LoginView):
    authentication_form = AuthenticationFormNew

    form_class = AuthenticationFormNew

    template_name = 'login2.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        ip_address = get_ip(self.request)
        ip_user = self.request.user
        time = timezone.localtime(timezone.now())
        user_agent = get_usera(self.request)
        print(user_agent.browser.family)
        UserAgent(user_id=ip_user, user_ip_address=ip_address, time=time,
                  # Accessing user agent's broswer properties
                  browser=user_agent.browser.family,  # returns 'Mobile Safari'
                  broswer_id=user_agent.browser.version_string,   # returns '5.1'
                  # Accessing user agent's operating system properties
                  os=user_agent.os.family,  # returns 'iOS'
                  os_id=user_agent.os.version_string,  # returns '5.1'
                  # Accessing user agent's device properties
                  device=user_agent.device.family,  # returns 'iPhone'
                  device_brand=user_agent.device.brand,  # returns 'Apple'
                  device_model=user_agent.device.model,  # returns 'iPhone'
                  location=get_geolocation_for_ip(ip_address)
                  ).save()

        return super(LoginView, self).form_valid(form)
