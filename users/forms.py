from typing import Any, Union

from django import forms
from django.contrib.auth import (authenticate, get_user_model,
                                 password_validation)
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.utils.text import capfirst

from users.models import CustomUser, Profile

UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email_confirmation = forms.EmailField(
        help_text="Enter your email again, for verfication.")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields.get('first_name').required = True
        self.fields.get('last_name').required = True

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'email_confirmation',
            'password1',
            'password2',
            'first_name',
            'last_name',
        ]

    def clean_email_confirmation(self):
        email = self.data.get('email')
        email_confirmation = self.data.get('email_confirmation')
        if email_confirmation != email:
            raise forms.ValidationError("Emails do not match.")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
        ]


class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autofocus': True})
    )

    field_order = ['email', 'password']

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')

        # Set the label for the "username" field.
        self.username_field = UserModel._meta.get_field(
            UserModel.USERNAME_FIELD)
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(
                self.username_field.verbose_name)

    def clean(self) -> Any:
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'avatar']


class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
