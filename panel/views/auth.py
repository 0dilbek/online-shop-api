from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('panel:dashboard')
        return render(request, 'panel/login.html')

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('panel:dashboard')
        return render(request, 'panel/login.html', {'error': "Login yoki parol noto'g'ri"})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('panel:login')
