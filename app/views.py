from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from app.models import Users

@csrf_exempt
def create_user(request):
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)

    try:
        payload = json.loads(request.body)
        username = payload["username"]
        password = payload["password"]
        role = payload["role"]
    except:
        return HttpResponse("missing/blank username, password, or role", status=401)

    if (username == "" or password == "" or role == ""):
        return HttpResponse("missing/blank username, password, or role", status=401)

    try:
        user_count = Users.objects.filter(username=username).count()
        if user_count != 0:
            return HttpResponse("username already in use", status=406)
    except Exception as e:
        return HttpResponse(status=401)

    user = Users(username=username, password=password, role=role)

    try:
        user.save()
        return HttpResponse("user succesfully created", status=201)
    except:
        return HttpResponse("error saving user", status=401)

@csrf_exempt
def login(request):
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)

    try:
        payload = json.loads(request.body)
        username = payload['username']
        password = payload['password']
    except:
        return HttpResponse("missing/blank username or password", status=401)

    try:
        user_count = Users.objects.filter(username=username, password=password).count()
        if user_count == 1:
            return HttpResponse("login successful", status=200)
        return HttpResponse("unable to find user", status=402)
    except:
        return HttpResponse("unable to find user", status=402)



    
    

# Create your views here.
