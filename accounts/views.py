from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        print(email, password, user)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'LandingPage')
            return redirect(next_url)
        else:
            return redirect('register_view')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:

            return render(request, 'register.html')

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name, last_name=surname)
        if user:
            return redirect('login_view')
        return render(request, 'register.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('LandingPage')