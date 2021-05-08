from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from secrets import token_bytes
import hmac
import hashlib
import time

from app.models import Users, UserAuthTokens

@csrf_exempt #NEED TO FIGURE OUT WHAT THIS IS!
def create_user(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)

    #input validation
    try:
        payload = json.loads(request.body)
        username = payload["username"]
        password = payload["password"]
        role = payload["role"]
    except:
        return HttpResponse("missing/blank username, password, or role", status=401)

    if (username == "" or password == "" or role == ""):
        return HttpResponse("missing/blank username, password, or role", status=401)

    #make sure username isn't already taken
    try:
        user_count = Users.objects.filter(username=username).count() 
        if user_count != 0:
            return HttpResponse("username already in use", status=406)
    except Exception as e:
        return HttpResponse(status=401)

    #save user in database
    user = Users(username=username, password=password, role=role)
    try:
        user.save()
        return HttpResponse("user succesfully created", status=201)
    except:
        return HttpResponse("error saving user", status=401)



@csrf_exempt
def login(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)

    #input validation
    try:
        payload = json.loads(request.body)
        username = payload['username']
        password = payload['password']
    except:
        return HttpResponse("missing/blank username or password", status=401)

    #make sure user exists
    try:
        user_count = Users.objects.filter(username=username, password=password).count()
        if user_count != 1:
            return HttpResponse("unable to find user", status=402)
    except:
        return HttpResponse("unable to find user", status=402)

    #create authentication token for session
    token = createAuthToken(username)

    request.session['username'] = username
    request.session['token'] = str(token)
    request.session.set_expiry(3600) #session expires in 3600 seconds = 1 hour

    return HttpResponse("login successful", status=200)


#this function is just used as a test to make sure the session authentication is working
@csrf_exempt
def auth_test(request):
    try:
        if checkAuthToken(request.session['username'], request.session['token']):
            return HttpResponse("authenticated", status=200)
    except:
        return HttpResponse("not authenticated", status=404)

    return HttpResponse("not authenticated", status=404)

#checks that the user's session is authenticated
def checkAuthToken(username, token):
    try:
        #get the most recent token entry in the database for the user
        userAndToken = UserAuthTokens.objects.filter(username=username).order_by('-timestamp')[0]
        
        tokenbytes = bytes(userAndToken.token, 'utf-8')

        #uses the same key as the createAuthToken method
        key = 'b\'\\xd3\\xf4\\xb7X\\xbd\\x07"\\xf4a\\\'\\xf5\\x16\\xd7a\\xa4\\xbd\\xf0\\xe7\\x10\\xdeR\\x0el\\xc2fW\\x80\\xfd\\xd39\\x953\''
        keybytes = bytes(key, 'utf-8')
        h = hmac.new( keybytes, tokenbytes, hashlib.sha256 )
        hashedToken = h.hexdigest()

        #compare_digest used to secure against timing attacks
        if hmac.compare_digest(token, str(hashedToken)):
            return True
        return False
    except Exception:
        return False

#creates the authentication token for sessions
def createAuthToken(username):
    #create secure 32 byte token
    token = str(token_bytes(32))
    userAndToken = UserAuthTokens(username=username, token=token, timestamp=time.time())
    
    userAndToken.save()

    #key generated using secrets.token_bytes(32)
    #32 byte key for encryption
    key = 'b\'\\xd3\\xf4\\xb7X\\xbd\\x07"\\xf4a\\\'\\xf5\\x16\\xd7a\\xa4\\xbd\\xf0\\xe7\\x10\\xdeR\\x0el\\xc2fW\\x80\\xfd\\xd39\\x953\''
    tokenbytes = bytes(token, 'utf-8')
    keybytes = bytes(key, 'utf-8')

    h = hmac.new( keybytes, tokenbytes, hashlib.sha256 )
    hashedToken = h.hexdigest()

    return hashedToken