from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login

def registroView(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            #user_auth=authenticate(user=user.username,password=user.password)
            login(request,user)
            return redirect("/?cuenta-nueva=true")
        else:
            return render(request=request,template_name="login/register-user.html",context={"form":form})

    form2 = UserCreationForm()
    return render(request=request,template_name="login/register-user.html",context={"form":form2})
