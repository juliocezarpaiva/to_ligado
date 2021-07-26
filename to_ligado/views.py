from django.shortcuts import render, redirect

def base(request):
    render(request, 'base.html')
    return redirect('home')

def home(request):
    return render(request, 'home.html')