from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from Ots.models import *
import random

def welcome(request):
    template=loader.get_template('welcome.html')
    return HttpResponse(template.render())

def candidateRegistrationForm(request):
    res=render(request,'registration_form.html')
    return res

def candidateRegistration(request):

    if request.method=='POST':
        #as we have filled the data int he form of post method thatswhy we used this POST dictionary

        username=request.POST['username']
        #now we are checking that whether the user is alredy exist or not
        if(len(Candidate.objects.filter(username=username))):
            userStatus=1
        else:
            candidate=Candidate()
            candidate.username=username
            candidate.password=request.POST['password']
            candidate.name=request.POST['name']
            candidate.save()
            userStatus=2

    else:
        userStatus=3  #means the value we get that havenot the post method it may be either get 

    context={
        'userStatus':userStatus
    }
    res=render(request,'registration.html',context)
    return res





def loginView(request):
    if request.method=='POST':
        
        username=request.POST['username']
        password=request.POST['password']
        candidate=Candidate.objects.filter(username=username,password=password)
        if(len(candidate)==0):
            #what if the login get failed 
            loginError="Invalid id or password"
            res=render(request,'login.html',{'loginError':loginError})
        else:
            #forr success case we are making tthe session variable to check that wheter the users are not acessing the resource without logging in
            request.session['username']=candidate[0].username
            request.session['name']=candidate[0].name
            res=HttpResponseRedirect("home")
    else:

        res=render(request,'login.html')
    return res

def candidateHome(request):
    if 'name' not in request.session.keys():
        #check that if you are on the home page then you are come after the login or not then returrn threm to login page 
        res=HttpResponseRedirect("login")
    else:
        res=render(request,'home.html')
    return res

def testPaper(request):
    if 'name' not in request.session.keys():
        #check that if you are on the home page then you are come after the login or not them return them to the login page 

        res=HttpResponseRedirect("login")

    #fetch question from database table 
    n=int(request.GET['n'])
    question_pools=list(Question.objects.all())
    random.shuffle(question_pools)
    questions_list=question_pools[:n]
    context={'questions':questions_list}
    res=render(request,'testpaper.html',context)
    return res
    

    

def calculateTestResult(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    total_attempt=0
    total_right=0
    total_wrong=0
    qid_list=[]
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))

    for n in qid_list:
        #here get return the object of the question directly
        question=Question.objects.get(qid=n)
        try:
            if question.ans==request.POST['q'+str(n)]:
                total_right+=1

            else:
                total_wrong+=1

            total_attempt+=1

        except:
            pass

    points=(total_right-total_wrong)/len(qid_list)*10

    #now store the result in the Result table
    result=Result()
    result.username=Candidate.objects.get(username=request.session['username'])

    result.attempt=total_attempt
    result.right=total_right
    result.wrong=total_wrong
    result.points=points
    result.save()

#updTING THE candidate table
    candidate=Candidate.objects.get(username=request.session['username'])
    candidate.test_attempt+=1
    candidate.points=(candidate.points*(candidate.test_attempt-1)+points)/candidate.test_attempt

    candidate.save()
    return HttpResponseRedirect('result')



def testResultHistory(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")

    candidate=Candidate.objects.filter(username=request.session['username'])
    results=Result.objects.filter(username_id=candidate[0].username)
    context={'candidate':candidate[0],'results':results}
    res=render(request,'candidate_history.html',context)
    return res



def showTestResult(request):
    if 'name' not in request.session.keys():
        res=render(request,"login")

    #fetch latest resul;t from teh result tabel 
    result=Result.objects.filter(resultid=Result.objects.latest('resultid').resultid,username_id=request.session['username'])
    context={'result':result}
    res=render(request,'show_result.html',context)
    return res


def logoutView(request):
    if 'name'  in request.session.keys():
        #check that if you are on the home page then you are come after the login or not with session key
        del request.session['username']
        del request.session['name']
    return HttpResponseRedirect("login")
    


