from django.shortcuts import render,redirect

# Create your views here.

def homeCapture(request):
    if request.user.is_authenticated:
        return render(request=request,template_name="cuentas/home.html")
    
    return redirect("login")