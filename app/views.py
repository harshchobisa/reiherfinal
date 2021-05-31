from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
import pandas as pd
import random

from secrets import token_bytes
import hmac
import hashlib
import string
import time
from matching.main import *
from matching.constants import *
# from matching.constants import *
# from matching.mentor import *
# from matching.mentee import *
# from matching.stable_match import *
# from sklearn.metrics.pairwise import euclidean_distances
# from matching.export import *

from django.middleware.csrf import get_token

from app.models import Users, UserAuthTokens, Mentors, Mentees, Pairings, PasswordReset

def index(request): 
    return render(request, "index.html")

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

    #make sure that more than one admin account cannot be created
    if role == "admin":
        try:
            user_count = Users.objects.filter(role=role).count() 
            if user_count > 0:
                return HttpResponse("cannot have multiple admins", status=406)
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
        #create authentication token for session
        token = createAuthToken(email)

        request.session['email'] = email
        request.session['token'] = str(token)
        request.session.set_expiry(1800) #session expires in 1800 seconds = 0.5 hour
        return HttpResponse("user succesfully created", status=201)
    except:
        return HttpResponse("error saving user", status=401)


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
    
    activitiesField = ['firstActivity', 'secondActivity', 'thirdActivity',
            'fourthActivity', 'fifthActivity']

    try:
        payload = json.loads(request.body)
        for field in requiredFields:
            if payload[field] == "":
                print(field)
                return HttpResponse("missing required fields lol", status=401)
        # activities_set = set()
        # for activity in activitiesField:
        #     activities_set.add(payload[activity])
        # if activities_set.size() != 5:
        #     return HttpResponse("invalid form response--give unique form responses", status=401)

    except:
        return HttpResponse("missing required fields hi", status=401)

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
    request.session.set_expiry(1800) #session expires in 1800 seconds = 0.5 hour

    return HttpResponse("login successful", status=200)


#this function is just used as a test to make sure the session authentication is working
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

def getFamily(familyid):
    try:
        family = Pairings.objects.filter(familyid=familyid)
        familyUsers = []
        for member in family:
            familyUsers.append(getUserInfo(member.email))
    except Exception:
        return None

    return familyUsers;


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
def getUserInfo(email, full=False):
    
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

    ##added a parameter to get all the values in json format
    if(full == True):
        info['gender'] = user.gender
        info['firstActivity'] = user.firstActivity
        info['secondActivity'] = user.secondActivity
        info['thirdActivity'] = user.thirdActivity
        info['fourthActivity'] = user.fourthActivity
        info['fifthActivity'] = user.fifthActivity
        if(role == "mentor"):
            info['mentorType'] = user.mentorType
        
        else:
            info['menteeType'] = user.menteeType
    return info

def convert_json(json_obj, mentor=True):
    return_array = []
    i = 0
    for elem in json_obj:
        temp_array = []
        if elem is not None:
            temp_array.append(elem.get('email', ''))
            temp_array.append(elem.get('firstName', ''))
            temp_array.append(elem.get('lastName', ''))
            temp_array.append(elem.get('year', ''))
            temp_array.append(elem.get('gender', ''))
            temp_array.append(elem.get('major', ''))
            if(mentor == True):
                temp_array.append(elem.get('mentorType', ''))
            else:
                temp_array.append(elem.get('menteeType', ''))
            temp_array.append(elem.get('firstActivity', ''))
            temp_array.append(elem.get('secondActivity', ''))
            temp_array.append(elem.get('thirdActivity', ''))
            temp_array.append(elem.get('fourthActivity', ''))
            temp_array.append(elem.get('fifthActivity', ''))
            return_array.append(temp_array.copy())
    if(mentor == True):
        matrix = pd.DataFrame(data=return_array, columns=['email', 'firstName', 'lastName', 'year', 'gender', 'major', 'mentorType', 'firstActivity', 'secondActivity', 'thirdActivity', 'fourthActivity', 'fifthActivity'])
    else:
        matrix = pd.DataFrame(data=return_array, columns=['email', 'firstName', 'lastName', 'year', 'gender', 'major', 'menteeType', 'firstActivity', 'secondActivity', 'thirdActivity', 'fourthActivity', 'fifthActivity'])
    return matrix

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
    
    # return populate_users(20, 79)
    # return HttpResponse("made users", status=200)
    try:
        mentor_objs = Mentors.objects.all()
    except Exception:
        print(Exception)
        return HttpResponse("error getting mentor objects", status=404)
    
    mentors = []
    for mentor in mentor_objs:
        mentors.append(getUserInfo(mentor.email, True))
    
    try:
        mentee_objs = Mentees.objects.all()
    except Exception:
        print(Exception)
        return HttpResponse("error getting mentee objects", status=404)
    
    mentees = []
    for mentee in mentee_objs:
        mentees.append(getUserInfo(mentee.email, True))

    mentors_array = convert_json(mentors)
    mentees_array = convert_json(mentees, False)

    familyToMentors, mentorEmailToMenteesEmails = matching_algorithm(mentors_array, mentees_array)
    mentee_emails = mentees_array['email'].to_list()
    paired_emails = []
    menteeCount = 0    
    for family_id in familyToMentors.keys():
        for mentor in familyToMentors[family_id]:
            mentor_email = mentor
            pair = Pairings(email=mentor, familyid=family_id)
            try:
                pair.save()
            except:
                return HttpResponse("error saving pairing", status=401)


            for mentee in mentorEmailToMenteesEmails[mentor_email]:
                paired_emails.append(mentee)
                pair = Pairings(email=mentee, familyid=family_id)
                try:
                    pair.save()
                except:
                    return HttpResponse("error saving pairing", status=401)
        print()
    
    missing_emails = list(set(mentee_emails) - set(paired_emails))
    last_family = len(familyToMentors)-1
    for mentee in missing_emails:
        rand_family = random.randint(0, last_family)
        pair = Pairings(email=mentee, familyid=family_id)
        try:
            pair.save()
        except:
            return HttpResponse("error saving pairing", status=401)

    return HttpResponse("successfully created all families", status=200)


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


def logout(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #only accept requests from users with a logged in, authenticated session
    if not checkAuthToken(request):
        return HttpResponse("user not authorized", status=401)

    try:
        del request.session['email']
        del request.session['token']
        return HttpResponse("success", status=200)
    except:
        return HttpResponse("error", status=404)

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


def create_mentors(num_mentors):
    for i in range(num_mentors):
        string_i = str(i)
        email_ = "mentor_{i}@gmail.com".format(i=string_i)
        firstName_ = "mentor"
        lastName_ = string_i
        rand_gender = random.randint(0,1)
        if(rand_gender == 0):
            gender_ = "Female"
        else:
            gender_ = "Male"
        rand_major = random.randint(0,10)
        major_ = categoryChoices['Majors'][rand_major]
        rand_type = random.randint(0,1)
        if(rand_type == 0):
            mentorType_ = "Academic"
        else:
            mentorType_ = "Social"
        year_list = ["2021", "2022", "2023"]
        rand_year = random.randint(0,2)
        year_ = year_list[rand_year]
        activities = categoryChoices['Activities']
        rand_activities = random.sample(range(0, 9), 5)
        firstActivity_ = activities[rand_activities[0]]
        secondActivity_ = activities[rand_activities[1]]
        thirdActivity_ = activities[rand_activities[2]]
        fourthActivity_ = activities[rand_activities[3]]
        fifthActivity_ = activities[rand_activities[4]]
        try:
            mentors = Mentors(email=email_, firstName=firstName_, lastName=lastName_, gender=gender_, major=major_, year=year_, firstActivity=firstActivity_, secondActivity=secondActivity_, thirdActivity=thirdActivity_, fourthActivity=fourthActivity_, fifthActivity=fifthActivity_, mentorType=mentorType_)
        except Exception as e:
            print(e)
        try:
            mentors.save()
        except Exception:
            return HttpResponse("unable to save mentors", 401)
        # print(major_)
    return HttpResponse("created mentors", 200)

def create_mentees(num_mentees):
    for i in range(num_mentees):
        string_i = str(i)
        email_ = "mentee_{i}@gmail.com".format(i=string_i)
        firstName_ = "mentee"
        lastName_ = string_i
        rand_gender = random.randint(0,1)
        if(rand_gender == 0):
            gender_ = "Female"
        else:
            gender_ = "Male"
        rand_major = random.randint(0,10)
        major_ = categoryChoices['Majors'][rand_major]
        rand_type = random.randint(0,1)
        if(rand_type == 0):
            menteeType_ = "Academic"
        else:
            menteeType_ = "Social"
        year_list = ["2023", "2024"]
        rand_year = random.randint(0,1)
        year_ = year_list[rand_year]
        activities = categoryChoices['Activities']
        rand_activities = random.sample(range(0, 9), 5)
        firstActivity_ = activities[rand_activities[0]]
        secondActivity_ = activities[rand_activities[1]]
        thirdActivity_ = activities[rand_activities[2]]
        fourthActivity_ = activities[rand_activities[3]]
        fifthActivity_ = activities[rand_activities[4]]
        try:
            mentees = Mentees(email=email_, firstName=firstName_, lastName=lastName_, gender=gender_, major=major_, year=year_, firstActivity=firstActivity_, secondActivity=secondActivity_, thirdActivity=thirdActivity_, fourthActivity=fourthActivity_, fifthActivity=fifthActivity_, menteeType=menteeType_)
        except Exception as e:
            print(e)
        try:
            mentees.save()
        except Exception:
            return HttpResponse("unable to save mentees", 401)
        # print(major_)
    return HttpResponse("created mentors and mentees", 200)
        

        

def populate_users(request):
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
        payload = json.loads(request.body)
        num_mentors = payload["num_mentors"]
        num_mentees = payload["num_mentees"]
    except:
        return HttpResponse("missing/blank email, password, or role", status=401)

    for i in range(num_mentors):
        string_i = str(i)
        email_ = "mentor_{i}@gmail.com".format(i=string_i)
        password_ = string_i
        key = 'b\'\\xd3\\xf4\\xb7X\\xbd\\x07"\\xf4a\\\'\\xf5\\x16\\xd7a\\xa4\\xbd\\xf0\\xe7\\x10\\xdeR\\x0el\\xc2fW\\x80\\xfd\\xd39\\x953\''
        passwordbytes = bytes(password_, 'utf-8')
        keybytes = bytes(key, 'utf-8')

        h = hmac.new( keybytes, passwordbytes, hashlib.sha256 )
        hashedPassword = str(h.hexdigest())
        role_ = "mentor"

        user = Users(email=email_, password=hashedPassword, role=role_)
        try:
            user.save()
        except:
            return HttpResponse("error saving user", status=401)
    for i in range(num_mentees):
        # print(i)
        string_i = str(i)
        email_ = "mentee_{i}@gmail.com".format(i=string_i)
        password_ = string_i
        key = 'b\'\\xd3\\xf4\\xb7X\\xbd\\x07"\\xf4a\\\'\\xf5\\x16\\xd7a\\xa4\\xbd\\xf0\\xe7\\x10\\xdeR\\x0el\\xc2fW\\x80\\xfd\\xd39\\x953\''
        passwordbytes = bytes(password_, 'utf-8')
        keybytes = bytes(key, 'utf-8')

        h = hmac.new( keybytes, passwordbytes, hashlib.sha256 )
        hashedPassword = str(h.hexdigest())
        role_ = "mentee"
        user = Users(email=email_, password=hashedPassword, role=role_)
        try:
            user.save()
        except:
            return HttpResponse("error saving user", status=401)
    create_mentors(num_mentors)
    return create_mentees(num_mentees)
    # return HttpResponse("succcesffuly did it", status=200)

def reset_password(request):

    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    #input validation
    try:
        payload = json.loads(request.body)
        email = payload['email']
        password = payload['password']
        token = payload['token']
    except:
        return HttpResponse("missing/blank email or token", status=401)

    #get the token from the database
    try:
        userAndToken = PasswordReset.objects.filter(email=email).filter(resetToken=token)[0]
    except:
        return HttpResponse("invalid token", status=401)
    
    #if token does not equal our database's token, reject
    if userAndToken.resetToken != token:
        return HttpResponse("invalid token", status=401)
    
    #check if token is expired or not
    if float(userAndToken.timestamp) < time.time():
        return HttpResponse("token expired", status=401)

    #delete token after it is used
    userAndToken.delete()


    #hash password
    key = 'b\'\\xd3\\xf4\\xb7X\\xbd\\x07"\\xf4a\\\'\\xf5\\x16\\xd7a\\xa4\\xbd\\xf0\\xe7\\x10\\xdeR\\x0el\\xc2fW\\x80\\xfd\\xd39\\x953\''
    passwordbytes = bytes(password, 'utf-8')
    keybytes = bytes(key, 'utf-8')

    h = hmac.new( keybytes, passwordbytes, hashlib.sha256 )
    hashedPassword = str(h.hexdigest())
    
    #save user in database
    user = Users.objects.get(email=email)
    user.password = hashedPassword

    try:
        user.save()
        return HttpResponse("password succesfully updated", status=201)
    except:
        return HttpResponse("error saving user", status=401)


#TODO change the responses for this method to all be identical
def request_password_reset(request):
    #only accept post requests
    if request.method != "POST":
        return HttpResponse("only POST calls accepted", status=404)
    
    try:
        payload = json.loads(request.body)
        email = payload['email']
    except:
        return HttpResponse("missing/blank email", status=401)

    #make sure user exists
    try:
        user_count = Users.objects.filter(email=email).count()
        if user_count != 1:
            return HttpResponse("unable to find user CHANGE THIS", status=200)
    except:
        return HttpResponse("unable to find user CHANGE THIS", status=200)

    #create secure token that is 20 chars long
    token = randStr(N=20)
    #this token will only be valid for 10 minutes
    passwordResetToken = PasswordReset(email=email, resetToken=token, timestamp=time.time() + 600)
    
    #save token in database for comparison
    passwordResetToken.save()
    
    sendResetEmail(email, token)
    return HttpResponse("email sent, token: " + token, status=200)

#sends a reset email given a token and an email
def sendResetEmail(email, token):
    import smtplib, ssl

    port = 465  # For SSL

    smtp_server = "smtp.gmail.com"
    sender_email = "mentorseas@gmail.com" 
    password = "Mentoring1$"

    receiver_email = email 

    #will have to change this upon deployment
    link = "localhost:8000/passwordResetPage/" + token
  
    subject = "MentorSeas Password Reset"
    text = "Hello, \n\nIf you are recieving this email, a password reset request has been sent for your account at MentorSeas. Follow the link to reset your password.\n\n{link}\n\nBest,\nBC Exec  "
    text = text.format(link=link)
    message = 'Subject: {}\n\n{}'.format(subject, text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()

#returns a randomly generated token of length N
def randStr(chars = string.ascii_uppercase + string.ascii_lowercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

def clear_pairings_database(request):
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


    try:
        Pairings.objects.all().delete()
    except:
        return HttpResponse("unable to delete pairings database", status=404)

    return HttpResponse("succesfully deleted pairings database", status=404)

@csrf_exempt
def get_csrf_token(request):
    token =  get_token(request)
    response = HttpResponse('success', status=200)
    # response.set_cookie('csrftoken', token)
    return response