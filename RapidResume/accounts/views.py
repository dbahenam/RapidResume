from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import RegisterForm

# Create your views here.

def login(request):
    next_page = request.GET.get('next','')
    
    # POST
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
    
    if user is not None:
        auth_login(request,user)

        # Check if the next_page url is safe for redirection
        if next_page and url_has_allowed_host_and_scheme(next_page, allowed_hosts={request.get_host()}):
            return redirect(next_page)
        else:
            return redirect('/home')
    
    # GET
    return render(request, 'login.html', {'next': next_page})

def sign_up(req):
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
    else:
        form = RegisterForm()
    return render(req, "registration/signup.html", {
        "form" : form
    })