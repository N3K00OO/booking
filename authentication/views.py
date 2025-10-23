from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from account.models import Profile 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        is_owner = request.POST.get("is_owner") == "true"

        # Validasi basic
        if not username or not password1 or not password2:
            return JsonResponse({"success": False, "error": "All fields are required."})

        if password1 != password2:
            return JsonResponse({"success": False, "error": "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "Username already taken."})

        # Create user
        user = User.objects.create_user(username=username, password=password1)
        profile = user.profile  # auto dibuat lewat signal
        profile.role = 'OWNER' if is_owner else 'USER'
        profile.save()

        return JsonResponse({"success": True, "message": "Account created successfully!"})

    return render(request, "register.html")

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login berhasil"})
        else:
            return JsonResponse({"success": False, "message": "Username atau password salah"})
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    if request.is_ajax():
        return JsonResponse({"success": True, "message": "Logout berhasil"})
    return redirect("login")