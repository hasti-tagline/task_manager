from django.shortcuts import render


# normal Django Views for open HTM pages.

def register_page(request):

    return render(request,"register.html")



def login_page(request):

    return render(request,"login.html")



def dashboard_page(request):

    return render(request,"dashboard.html")



