from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    username = forms.CharField(label=_('Ваше имя'),
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    password1 = forms.CharField(label=_('Пароль'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})))
    password2 = forms.CharField(label=_('Подтвердите пароль'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})))

    class Meta:
        model = User
        TextAttrib = {'class': 'form-control', 'type': 'text'}
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Создать аккаунт'))
        self.helper.label_class = 'col-lg-10'
        self.helper.field_class = 'col-lg-15'
        self.helper.form_class = 'form-group mb-3'


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Ваше имя'),
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    password = forms.CharField(label=_('Пароль'),
                               widget=(forms.PasswordInput(attrs={'class': 'form-control'})))

    class Meta:
        model = User
        TextAttrib = {'class': 'form-control', 'type': 'text'}
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-12 text-center'
        self.helper.field_class = 'col-lg-15'
