from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import pandas as pd
import pickle
from django.views import View
from .models import Heart
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from app1.forms import HeartForm
from app1.models import Heart

@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html', {'navbar': 'home'})

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if pass1!=pass2:
            return HttpResponse("You password and confrom password are not Same!! ")
        
        if User is not None:
        #      return HttpResponse("Harap isi dengan benar !!")
        # else: 
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
        
        
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass') 
        User=authenticate(request,username=username,password=pass1)
        if User is not None:
            login(request,User)
            return redirect('home') 
        else:
            return HttpResponse("Username or Password is incorrect!!!")
         
    return render (request,'login.html')

def PredictPage(request):
    return render(request,'predict.html', {'navbar': 'predict'})

def result(request):
    print(request)
    age = int(request.POST.get('age'))
    sex = int(request.POST.get('sex'))
    cp = int(request.POST.get('cp'))
    trestbps = int(request.POST.get('trestbps'))
    chol = int(request.POST.get('chol'))
    fbs = int(request.POST.get('fbs'))
    restecg = int(request.POST.get('restecg'))
    thalach = int(request.POST.get('thalach'))
    exang = int(request.POST.get('exang'))
    oldpeak = int(request.POST.get('oldpeak'))
    slope = int(request.POST.get('slope'))
    ca = int(request.POST.get('ca'))
    thal = int(request.POST.get('thal'))
    target = int(request.POST.get('target'))
    model = pd.read_pickle("./models/model4.pickle")
    result = model.predict([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,
                             oldpeak,slope,ca,thal,target]])
    return render(request, 'result.html', {'result':result})
    
def ReportPage(request):
    return render (request,'report.html', {'navbar': 'report'})

def LogoutPage(request):
    logout(request)
    return redirect('login')



### IMPLEMENTASI CRUD
def heart(request):
    if request.method == "POST":
        form = HeartForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/viewdata')
            except:
                pass
    else:
        form = HeartForm()
    return render(request, 'haltambah.html', {'form': form})

def viewdata(request):
    heart = Heart.objects.all()
    return render(request, "view.html", {'heart': heart})


def delete(request, id):
    heart = Heart.objects.get(id=id)
    heart.delete()
    return redirect("/view")


def edit(request, id):
    heart = Heart.objects.get(id=id)
    return render(request, 'edit.html', {'heart': heart})

def update(request, id):
    heart = Heart.objects.get(id=id)
    form = HeartForm(instance=heart)

    if request.method == 'POST':
        form = HeartForm(request.POST, instance=heart)
        if form.is_valid():
            form.save()
            return redirect('/viewdata')
    return render(request, 'view.html', {'form': form})

