from django.shortcuts import render
from .forms import RegisterForm
# Create your views here.


def sign_up(req):
    if req.method == "POST":
        form = RegisterForm(req.POST)
    else:
        form = RegisterForm()
    return render(req, "registration/signup.html", {
        "form" : form
    })