from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from secrets import token_bytes
import hmac
import hashlib
import time

from app.models import Users, UserAuthTokens, Mentors, Mentees, Pairings

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


@csrf_exempt
def get_all_families(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #only accept requests from users with a logged in, authenticated session
    if not checkAuthToken(request):
        return HttpResponse("user not authorized", status=401)

    #make sure this api is only accessible to admins
    try:
        user = Users.objects.get(email=request.session["email"])
        if user.role != "admin":
            return HttpResponse("not authorized--must be admin to see all families", status=401)

    except Exception:
        return HttpResponse("unable to find user", status=404)

    try:
        familyids = Pairings.objects.values_list('familyid', flat=True).distinct()
    except Exception:
        print(Exception)
        return HttpResponse("error getting family ids", status=404)
    
    allFamilies = []
    try:
        for id in familyids:
            allFamilies.append(getFamily(id))
    except Exception:
        print(Exception)
        return HttpResponse("error getting families", status=404)

    return JsonResponse(allFamilies, safe=False)



@csrf_exempt
def get_user_family(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #only accept requests from users with a logged in, authenticated session
    if not checkAuthToken(request):
        return HttpResponse("user not authorized", status=401)

    #input validation
    try:
        email = request.session['email']
    except:
        return HttpResponse("missing required fields", status=401)

    #get the user's familyid
    print("email")
    try:
        familyid = Pairings.objects.get(email=request.session["email"]).familyid
    except Exception:
        print(Exception)
        return HttpResponse("user has not been assigned to family", status=404)
    
    #using the user's familyid, get all members in the family
    try:
        familyUsers = getFamily(familyid)
    except Exception:
        return HttpResponse("error getting user's family", status=404)
    
    return JsonResponse(familyUsers, safe=False)


#get a single user's info, given the user's email
def getUserInfo(email):
    
    #get the user's role so we know which table to look in
    try:
        user = Users.objects.get(email=email)
    except:
        return None
    
    role = user.role

    if role == "mentor":
        user = Mentors.objects.get(email=email)
    elif role == "mentee":
        user = Mentees.objects.get(email=email)
    else: #should never hit this
        return None

    info = {}

    info['email'] = email
    info['firstName'] = user.firstName
    info['lastName'] = user.lastName
    info['year'] = user.year
    info['major'] = user.major
    info['role'] = role

    return info

#gets a family given the familyid
def getFamily(familyid):
    try:
        family = Pairings.objects.filter(familyid=familyid)
        familyUsers = []
        for member in family:
            familyUsers.append(getUserInfo(member.email))
    except Exception:
        return None

    return familyUsers;


@csrf_exempt
def create_families(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #only accept requests from users with a logged in, authenticated session
    if not checkAuthToken(request):
        return HttpResponse("user not authorized", status=401)

    #make sure this api is only accessible to admins
    try:
        user = Users.objects.get(email=request.session["email"])
        if user.role != "admin":
            return HttpResponse("not authorized--must be admin to create families", status=401)

    except Exception:
        return HttpResponse("unable to find user", status=404)


    return HttpResponse("families succesfully created", status=200)


@csrf_exempt
def has_completed_profile(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #only accept requests from users with a logged in, authenticated session
    if not checkAuthToken(request):
        return HttpResponse("user not authorized", status=401)

    #input validation
    try:
        email = request.session['email']
    except:
        return HttpResponse("missing required fields", status=401)
        
    #get the user's role so we know which table to look in
    try:
        user = Users.objects.get(email=email)
    except:
        return None
    
    role = user.role

    #look for this user in mentor and mentee database
    try:
        if role == "mentor":
            user = Mentors.objects.get(email=email)
            if user:
                return HttpResponse(True, status=200)
        elif role == "mentee":
            user = Mentees.objects.get(email=email)
            if user:
                return HttpResponse(True, status=200)
        return HttpResponse(False, status=200)
    except:
        return HttpResponse(False, status=200)


@csrf_exempt
def is_mentor(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #only accept requests from users with a logged in, authenticated session
    if not checkAuthToken(request):
        return HttpResponse("user not authorized", status=401)

    #input validation
    try:
        email = request.session['email']
    except:
        return HttpResponse("missing required fields", status=401)
        
    #get the user's role so we know which table to look in
    try:
        user = Users.objects.get(email=email)
    except:
        return None
    
    role = user.role

    if role == "mentor":
        return HttpResponse(True, status=200)
    else:
        return HttpResponse(False, status=200)


@csrf_exempt
def logout(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #only accept requests from users with a logged in, authenticated session
    if not checkAuthToken(request):
        return HttpResponse("user not authorized", status=401)

    try:
        del request.session['email']
        return HttpResponse("success", status=200)
    except:
        return HttpResponse("error", status=404)

@csrf_exempt
def get_current_user(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #only accept requests from users with a logged in, authenticated session
    if not checkAuthToken(request):
        return HttpResponse("user not authorized", status=401)

    try:
        email = request.session['email']
        return HttpResponse(email, status=200)
    except:
        return HttpResponse("unable to get current user", status=404)

