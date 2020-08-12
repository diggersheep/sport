
# Create your views here.
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from sport import settings


class LoginView(TemplateView):
    template_name = 'forms/login.html'
    redirect = '/'

    def post(self, request, **kwargs):
        from django.contrib.auth import authenticate

        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(
            username=username,
            password=password
        )
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(self.redirect)
        return render(request, self.template_name)


class LogoutView(TemplateView):
    template_name = 'logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
