from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from registration.forms import SignUpForm, LoginForm


class MySignupView(CreateView):
    form_class = SignUpForm
    success_url = '/registration/login'
    template_name = 'registration/signup.html'


class MyLoginView(LoginView):
    form_class = LoginForm
    success_url = '/mycompany/'
    template_name = 'registration/login.html'
