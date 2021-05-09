from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from secrets import token_bytes
import hmac
import hashlib
import time

from app.models import Users, UserAuthTokens, Mentors, Mentees

@csrf_exempt #NEED TO FIGURE OUT WHAT THIS IS!
def create_user(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)

    #input validation
    try:
        payload = json.loads(request.body)
        email = payload["email"]
        password = payload["password"]
        role = payload["role"]
    except:
        return HttpResponse("missing/blank email, password, or role", status=401)

    if (email == "" or password == "" or role == ""):
        return HttpResponse("missing/blank email, password, or role", status=401)

    #make sure email isn't already taken
    try:
        user_count = Users.objects.filter(email=email).count() 
        if user_count != 0:
            return HttpResponse("email already in use", status=406)
    except Exception as e:
        return HttpResponse(status=401)


    #hash password
    key = 'b\'\\xd3\\xf4\\xb7X\\xbd\\x07"\\xf4a\\\'\\xf5\\x16\\xd7a\\xa4\\xbd\\xf0\\xe7\\x10\\xdeR\\x0el\\xc2fW\\x80\\xfd\\xd39\\x953\''
    passwordbytes = bytes(password, 'utf-8')
    keybytes = bytes(key, 'utf-8')

    h = hmac.new( keybytes, passwordbytes, hashlib.sha256 )
    hashedPassword = str(h.hexdigest())
    


    #save user in database
    user = Users(email=email, password=hashedPassword, role=role)
    try:
        user.save()
        return HttpResponse("user succesfully created", status=201)
    except:
        return HttpResponse("error saving user", status=401)

@csrf_exempt
def create_mentor(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #only accept requests from users with a logged in, authenticated session
    if not checkAuthToken(request):
        return HttpResponse("user not authorized", status=401)

    #input validation
    requiredFields = ['firstName', 'lastName', 'year', 
            'gender', 'major', 'mentorType', 'firstActivity', 'secondActivity', 'thirdActivity',
            'fourthActivity', 'fifthActivity']
    try:
        payload = json.loads(request.body)
        for field in requiredFields:
            if payload[field] == "":
                return HttpResponse("missing required fields", status=401)
    except:
        return HttpResponse("missing required fields", status=401)

    #make sure this api is only accessible to mentors
    try:
        user = Users.objects.get(email=request.session["email"])
        print(user.role)
        if user.role != "mentor":
            return HttpResponse("not authorized--must be a mentor to create mentor profile", status=401)

    except Exception:
        # print(Exception.with_traceback)
        return HttpResponse("unable to find user", status=404)
    

    #!TODO do some primary/foreign key business to make sure unique emails being inserted

    #save mentor in database
    mentor = Mentors(email=request.session["email"],firstName=payload["firstName"],lastName=payload["lastName"],year=payload["year"],
        gender=payload["gender"],major=payload["major"],mentorType=payload["mentorType"],
        firstActivity=payload["firstActivity"],secondActivity=payload["secondActivity"],thirdActivity=payload["thirdActivity"],
        fourthActivity=payload["fourthActivity"],fifthActivity=payload["fifthActivity"])

    try:
        mentor.save()
        return HttpResponse("mentor succesfully created", status=201)
    except:
        return HttpResponse("error saving user", status=401)

@csrf_exempt
def create_mentee(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #only accept requests from users with a logged in, authenticated session
    if not checkAuthToken(request):
        return HttpResponse("user not authorized", status=401)

    # input validation
    requiredFields = ['firstName', 'lastName', 'year', 
            'gender', 'major', 'menteeType', 'firstActivity', 'secondActivity', 'thirdActivity',
            'fourthActivity', 'fifthActivity']
    try:
        payload = json.loads(request.body)
        for field in requiredFields:
            if payload[field] == "":
                return HttpResponse("missing required fields", status=401)
    except:
        return HttpResponse("missing required fields", status=401)
    
    #make sure this api is only accessible to mentees
    try:
        user = Users.objects.get(email=request.session["email"])
        if user.role != "mentee":
            return HttpResponse("not authorized--must be a mentee to create mentee profile", status=401)

    except:
        return HttpResponse("unable to find user", status=404)

    #!TODO do some primary/foreign key business to make sure unique emails being inserted

    #save mentee in database
    mentee = Mentees(email=request.session["email"],firstName=payload["firstName"],lastName=payload["lastName"],year=payload["year"],
        gender=payload["gender"],major=payload["major"],menteeType=payload["menteeType"],
        firstActivity=payload["firstActivity"],secondActivity=payload["secondActivity"],thirdActivity=payload["thirdActivity"],
        fourthActivity=payload["fourthActivity"],fifthActivity=payload["fifthActivity"])

    try:
        mentee.save()
        return HttpResponse("mentee succesfully created", status=201)
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
        email = payload['email']
        password = payload['password']
    except:
        return HttpResponse("missing/blank email or password", status=401)

    #hash password
    key = 'b\'\\xd3\\xf4\\xb7X\\xbd\\x07"\\xf4a\\\'\\xf5\\x16\\xd7a\\xa4\\xbd\\xf0\\xe7\\x10\\xdeR\\x0el\\xc2fW\\x80\\xfd\\xd39\\x953\''
    passwordbytes = bytes(password, 'utf-8')
    keybytes = bytes(key, 'utf-8')

    h = hmac.new( keybytes, passwordbytes, hashlib.sha256 )
    hashedPassword = str(h.hexdigest())
    

    #make sure user exists
    try:
        user_count = Users.objects.filter(email=email, password=hashedPassword).count()
        if user_count != 1:
            return HttpResponse("unable to find user", status=404)
    except:
        return HttpResponse("unable to find user", status=404)

    #create authentication token for session
    token = createAuthToken(email)

    request.session['email'] = email
    request.session['token'] = str(token)
    request.session.set_expiry(3600) #session expires in 3600 seconds = 1 hour

    return HttpResponse("login successful", status=200)


#this function is just used as a test to make sure the session authentication is working
@csrf_exempt
def auth_test(request):
    try:
        if checkAuthToken(request.session['email'], request.session['token']):
            return HttpResponse("authenticated", status=200)
    except:
        return HttpResponse("not authenticated", status=404)

    return HttpResponse("not authenticated", status=404)

#checks that the user's session is authenticated
def checkAuthToken(request):
    try:
        email = request.session['email'] 
        token = request.session['token']
        #get the most recent token entry in the database for the user
        userAndToken = UserAuthTokens.objects.filter(email=email).order_by('-timestamp')[0]
        
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
def createAuthToken(email):
    #create secure 32 byte token
    token = str(token_bytes(32))
    userAndToken = UserAuthTokens(email=email, token=token, timestamp=time.time())
    
    #save token in database for comparison
    userAndToken.save()

    #key generated using secrets.token_bytes(32)
    #32 byte key for encryption
    key = 'b\'\\xd3\\xf4\\xb7X\\xbd\\x07"\\xf4a\\\'\\xf5\\x16\\xd7a\\xa4\\xbd\\xf0\\xe7\\x10\\xdeR\\x0el\\xc2fW\\x80\\xfd\\xd39\\x953\''
    tokenbytes = bytes(token, 'utf-8')
    keybytes = bytes(key, 'utf-8')

    h = hmac.new( keybytes, tokenbytes, hashlib.sha256 )
    hashedToken = h.hexdigest()

    return hashedToken