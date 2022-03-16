from django.shortcuts import render, redirect
from . models import User
import bcrypt
from django.contrib import messages
from django.contrib.messages import get_messages

# Display Methods
def index(request):
    uid = request.session.get('userID')
    if uid is not None:
        return redirect("/success")
    else:
        return render(request, "index.html")

def success(request):
    uid = request.session.get('userID')
    if uid is not None:
        thisUser = User.objects.get(id=uid)
        context = {
            'thisUser': User.objects.get(id=uid)
        }
        return render(request, "success.html", context)
    else:
        return redirect("/")

# Action Methods
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            birthday = request.POST['birthday'],
            password = hash_pw
        )
        request.session['userID'] = new_user.id
        return redirect("/success")

def login(request):
    existing_user = User.objects.filter(email=request.POST['email']).first()
    errors = User.objects.login_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    if existing_user is not None:
        if bcrypt.checkpw(request.POST['password'].encode(), existing_user.password.encode()):
            request.session['userID'] = existing_user.id
            return redirect("/success")
        else:
            print('password does not match')
            return redirect("/")
    else:
        return redirect("/")

def log_out(request):
    request.session.clear()
    return redirect("/")