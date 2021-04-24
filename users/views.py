from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from users.models import CustomUser, Profile

from .forms import ConfirmPasswordForm, CustomUserCreationForm, ProfileForm
from .models import CustomUser
from .tokens import account_activation_token


def register(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        registration_form = CustomUserCreationForm()
        profile_form = ProfileForm()
    else:
        registration_form = CustomUserCreationForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        if registration_form.is_valid() and profile_form.is_valid():
            new_user: CustomUser = registration_form.save(commit=False)
            profile: Profile = profile_form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            profile.user = new_user
            profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            template_name = 'registration/activate_email.html'
            context = {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            }
            message = render_to_string(template_name, context)
            to_email = registration_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject,
                message,
                to=[to_email]
            )
            email.send()
            messages.success(
                request, 'You are now registered! Please confirm your email.')
            return render(request, 'registration/confirm.html', {'email': to_email})
    context = {'form': registration_form, 'profile_form': profile_form}
    return render(request, 'registration/register.html', context)


def activate(request: HttpRequest, uidb64: bytes, token: str):
    try:
        user_id = urlsafe_base64_decode(force_text(uidb64))
        user = get_object_or_404(CustomUser, id=user_id)
    except (TypeError, ValueError, OverflowError, Http404):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Successfully activated your account.')
        return redirect('news:home')
    else:
        return HttpResponse('<h1>Sorry, but the activation link was invalid.</h1>')


def profile(request: HttpRequest, email: str) -> HttpResponse:
    user = get_object_or_404(CustomUser, email=email)
    context = {'user': user}
    return render(request, 'registration/profile.html', context)


@login_required
def delete_account(request: HttpRequest, email: str):
    user = get_object_or_404(CustomUser, email=email)
    if user != request.user:
        raise Http404
    if request.method != 'POST':
        form = ConfirmPasswordForm()
    else:
        form = ConfirmPasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if not user.check_password(password):
                messages.error(
                    request, 'Password incorrect. Please try again.')
                context = {'user': user, 'form': form}
                return render(request, 'registration/delete-account.html', context)
            user.delete()
            messages.success(request, 'Your account was deleted.')
            return redirect('news:home')
    context = {'user': user, 'form': form}
    return render(request, 'registration/delete-account.html', context)


@login_required
def edit_profile(request: HttpRequest, email: str):
    user = get_object_or_404(CustomUser, email=email)
    if user != request.user:
        raise Http404
    profile = user.profile
    if request.method != 'POST':
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm(
            instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('users:profile', email=user.email)
    context = {'form': form, 'user': user}
    return render(request, 'registration/edit-profile.html', context)


@login_required
def change_password(request: HttpRequest):
    if request.method != 'POST':
        form = PasswordChangeForm(user=request.user)
    else:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('users:profile', email=request.user.email)
        else:
            messages.error(request, 'Please correct the below errors.')
    context = {'form': form}
    return render(request, 'registration/change-password.html', context)
