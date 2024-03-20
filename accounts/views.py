from django.shortcuts import render
from django.views import View

from accounts.forms import RegistrationForm


# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('success')  # Przekierowanie do strony sukcesu
        return render(request, 'register.html', {'form': form})