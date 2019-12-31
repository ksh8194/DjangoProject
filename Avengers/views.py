from django.shortcuts import render, redirect
#from calendar import Calendar as c2
import calendar as c1
import datetime as d1
from Avengers.models import Schedule, Myinfo
from django.http.response import HttpResponse
import json
from requests.sessions import session

# Create your views here.

def MainFunc(request):
    return render(request,'login.html')

def RegisterFunc1(request):
    return render(request,'register.html')

def RegisterFunc2(request):
    email = request.POST.get("email")
    password = request.POST.get("passwd")
    repassword = request.POST.get("repasswd")
    rdata = Myinfo(email=email,pwd=password)
    rdata.save()

    return render(request,'login.html')

def SelectedFunc(request):
    email = request.session.get("email")
    stemp = Schedule.objects.all().order_by('-star')
    date = request.GET.get('date')
   
    schedule = [email, 'yes']
    for s in stemp:
        dateFromDb = str(s.date).split(' ')[0].split('-')[2]
        if int(dateFromDb) < 10:
            if s.memid.email == email and dateFromDb[1] == date: 
                schedule.append({'title' : s.title, 'content' : s.content, 'star' : s.star})
        else:
            if s.memid.email == email and dateFromDb == date: 
                schedule.append({'title' : s.title, 'content' : s.content, 'star' : s.star})    
    
    if len(schedule) == 2:
        schedule=[email, 'no', {'content' : '등록된 스케줄이 없습니다'}]
                
    return HttpResponse(json.dumps(schedule), content_type="application/json")
   


def CalendarFunc(request):

    if request.GET.get('month') == 'plus':
        request.session['monthcnt'] = 1 
    elif request.GET.get('month') == 'minus':
        request.session['monthcnt'] = -1
 
    email = request.session.get('email')
   
    year = request.session['year']
    month = request.session['month']
    

    if month+request.session['monthcnt'] > 12:
        
        request.session['month'] = 1
        request.session['year'] = request.session['year'] + 1 
        month = 1
        year = year + 1
        
    elif month+request.session['monthcnt'] == 0:
        request.session['month'] = 12
        request.session['year'] = request.session['year'] - 1
        month = 12
        year = year - 1
        
    
    elif month+request.session['monthcnt'] <= 12:
        month = month + request.session['monthcnt']
        request.session['month'] = month
    

    cal = c1.Calendar(0)
    tempList = cal.itermonthdays4(year, month)
    dayList = []
    for v in tempList:
        if v[1] == month:
            dayList.append(v)    

    memid = Myinfo.objects.filter(email=email)[0].id #로그인 한 유저의 pk추출
    dateFromDb = Schedule.objects.filter(memid=memid) #로그인 한 유저의 전체 스케줄
    scheduleDay = []
    for d in dateFromDb:
        #로그인 한 유저의 이번달에 대한 스케줄
        yearFromDb = str(d.date).split(' ')[0].split('-')[0]
        monthFromDb = str(d.date).split(' ')[0].split('-')[1]
        if int(monthFromDb) < 10:
            monthFromDb = monthFromDb[1]
        if yearFromDb == str(year) and monthFromDb == str(month):
            #로그인 한 유저의 이번달 스케줄 날짜 추출
            day = str(d.date).split(' ')[0].split('-')[2]
            
            if day[0] == '0':
                if len(scheduleDay) == 0:
                        scheduleDay.append(int(day[1]))

                else:
                    for s in scheduleDay:
                        if int(day[1]) != s:
                            scheduleDay.append(int(day[1]))
            else:
                if len(scheduleDay) == 0:
                        scheduleDay.append(int(day))
                else:
                    for s in scheduleDay:
                        if int(day) != s:
                            scheduleDay.append(int(day))

    password = request.session["passwd"]
    myinfo = Myinfo.objects.all()
    count = 0
    param = {}
    
    scheduleDay = (list(set(scheduleDay)))
    
    for a in myinfo:
       
        if email==a.email and password == a.pwd:
            count = count+1   
         
        if(count!=0):
            target = 'main.html'
            param = {'email' : email, 'dayList' : dayList, 'scheduleDay' : scheduleDay}
        else:
            target = 'error.html'
            param = {}
 
    return HttpResponse(json.dumps(param), content_type="application/json")
    #return render(request, target, param)
 


def LoginFunc(request):
    if request.GET.get('month') == 'plus':
        request.session['monthcnt'] = request.session['monthcnt'] + 1 
    elif request.GET.get('month') == 'minus':
        request.session['monthcnt'] = request.session['monthcnt'] - 1
    else:
        request.session['monthcnt'] = 0
    if request.GET.get('flag'):
        pass
    else:   
        request.session['email'] = request.POST.get('email')
        request.session['passwd'] = request.POST.get('passwd')
    
    email = request.session.get('email')
    password = request.session["passwd"]

    today = str(d1.date.today()).split('-')
     
    year = int(today[0])
    month = int(today[1])
    
    request.session['year'] = year
    request.session['month'] = month    
    
    if month+request.session['monthcnt'] > 12:
        month = month+request.session['monthcnt']-12
        year = year + 1

    cal = c1.Calendar(0)
    tempList = cal.itermonthdays4(year, month)
    dayList = []
    for v in tempList:
        if v[1] == int(month):
            dayList.append(v)    
 
    memid = Myinfo.objects.filter(email=email)[0].id #로그인 한 유저의 pk추출
    dateFromDb = Schedule.objects.filter(memid=memid) #로그인 한 유저의 전체 스케줄
    scheduleDay = []
    for d in dateFromDb:
        if str(d.date).split(' ')[0].split('-')[0] == str(year) and str(d.date).split(' ')[0].split('-')[1] == str(month):
            day = str(d.date).split(' ')[0].split('-')[2]

            if day[0] == '0':
                if len(scheduleDay) == 0:
                        scheduleDay.append(int(day[1]))
                else:
                    for s in scheduleDay:
                        if int(day[1]) != s:
                            scheduleDay.append(int(day[1]))
                            
            else:
                if len(scheduleDay) == 0:
                        scheduleDay.append(int(day))
                else:
                    for s in scheduleDay:
                        if int(day) != s:
                            scheduleDay.append(int(day))
                        
    password = request.session["passwd"]
    myinfo = Myinfo.objects.all()
    count = 0
    param = {}
    
    scheduleDay = (list(set(scheduleDay)))
    length = []
 
    for a in myinfo:
       
        if email==a.email and password == a.pwd:
            count = count+1   
         
        if(count!=0):
            target = 'main.html'
            param = {'email' : email, 'dayList' : dayList, 'scheduleDay' : scheduleDay}
        else:
            target = 'error.html'
            param = {}
   
    return render(request, target, param)
 


def LogoutFunc(request):
    request.session.modified = True
    del request.session['email']
    del request.session['passwd']
    del request.session['year']
    del request.session['month']
    return redirect('/')      

def DeleteFunc(request):
    memid = Myinfo.objects.filter(email=request.session['email'])[0].id #로그인 한 유저의 pk추출
    dels = Schedule.objects.filter(memid=memid)
    email = request.session['email']
    passwd = request.session['passwd']
    for d in dels:
        if d.content == request.GET.get('del'):
            d.delete()
    return redirect('/go/login?flag=yes')

def InsertFunc1(request):
    return render(request,'insert.html')



def InsertFunc2(request):

    myinfo = Myinfo.objects.all()
    memid = 0
    for a in myinfo:
        if a.email==request.session['email']:
            memid = a
          
    title = request.POST.get('title')
    content = request.POST.get('content')
    date = request.POST.get('datePicker') + (' 00:00:00')
    star = request.POST.get('count')

    sdata = Schedule(memid=memid,title=title,content=content,date=date,star=star)
    sdata.save()
    return redirect('/go/login?flag=yes')