from django.shortcuts import render, redirect
from django.conf import settings
from .forms import AuthorizationForm, SearchForm, PasingForm, ResumeForm, ResumeRecord
from .services import OriginParsing, OrigenUrl, OrigenRequest ##SearchingService, ResumeParsService
from django.contrib.auth import authenticate, login
from .models import Resume, ResumeLink, TableColumnHead
from django.http import JsonResponse
import datetime
import re
from .models import Domain, SearchObject, VailidValues, SchemaParsing, Credentials, RequestHeaders, SessionData, CredentialsData, SearchCard, list_of_value, SearchResult
from .services import LoginServer
import json
from django.forms.models import BaseModelFormSet, modelformset_factory


def Test(request):
    ResumeFormSet = modelformset_factory(Resume, form=ResumeForm)
    return render(request, 'blog/test.html', { 'formset' : ResumeFormSet })
    
def authorization(request):
    if(request.method == 'GET'):
        authForm = AuthorizationForm()
        return render(request, 'blog/auth.html', { 'form' : authForm})
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                authForm = AuthorizationForm()
                return render(request, 'blog/auth.html', { 'form' : authForm, 'message' : u'Учетная запись неактивна, обратитесь к администратору'})
        else:
            authForm = AuthorizationForm()
            return render(request, 'blog/auth.html', { 'form' : authForm, 'message' : u'Введено некорректное имя пользователя или пароль'})

            
def exit(request):
    if not request.user.is_authenticated():
        logout(request)
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
def homespace(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        date = datetime.datetime.today().strftime('%d-%m-%Y')
        return render(request, 'blog/index.html', {'date' : date})

def searchForm(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        form = SearchForm()
        return render(request, 'blog/search_form.html', {'form' : form})
        
def searchOrigen(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        
    if(request.method == "GET"):
        errorStack = []
        data = {key : request.GET.get(key) for key in ('text','ageTo','ageFrom','salaryTo','salaryFrom', 'gender', 'searchMode')} ##limit, itemPage
        form = SearchForm(data)
        form.is_valid()
        dataParm = {key.lower() : data[key] for key in data}
        source = request.GET.get('source')
        task_id = request.GET.get('task_id')
        limit = 20
        
        if((task_id is not None) and (task_id != '')):
            search_card = SearchCard.objects.filter(id=task_id)
        else:
            query = SearchCard.objects.filter(text=data['text'], ageFrom=data['ageFrom'], ageTo=data['ageTo'], 
            salaryFrom=data['salaryFrom'], salaryTo=data['salaryTo'], gender=data['gender'])
            
            if query.count() == 0:
                search_card = SearchCard.objects.create(text=data['text'], ageFrom=data['ageFrom'], ageTo=data['ageTo'], 
                salaryFrom=data['salaryFrom'], salaryTo=data['salaryTo'], gender=data['gender'])##None
                search_card.save()
            else:
                search_card = query[0]
            
        if(source == 'all'):
            domainList = [item.name for item in list_of_value.objects.filter(type='SOURCE_LIST') if item.name != 'all']
        else:
            domainList = source.split(',')

        
        if(not domainList):
            errorMessage = "Произошла ошибка! Не был задан источник резюме"
            errorStack.append(errorMessage)
            return render(request, 'blog/search_response.html', {'form': form, 'errors': errorStack})

            
        ##По идее эта штука должна выполняться параллельно
        requestList = []
        emptyCount = 0
        
        for domainName in domainList:
            domain = Domain.objects.get(domainName=domainName, inactive=False)
            query_result = SearchResult.objects.filter(search_card=search_card, domain=domain)##added=False, hidden=False)
            
            if query_result.count() == 0:
                parser = OriginParsing(domain, limit, "SEARCH", search_card)
                parser.generalSchem()
                parser.setErrorTarget()
                parser.setBodyResponceTarget()
                linkOrigen = OrigenUrl(domain=domain)
                linkOrigen.createSearchLink(dataParm, data)
                requestOrig = OrigenRequest(domain,linkOrigen)
                while(parser.countResume < limit):
                    
                    requestTree = requestOrig.request()
                    print('------------------')
                    requestItem = parser.parsingResume(requestTree)
                    
                    if(requestItem):
                        requestList += requestItem
                    else:
                        emptyCount += 1
                    
                    if(emptyCount > 5):
                        errorMessage = 'В настоящее время сервер %s недоступен по техническим пречинам' % domain.domainName
                        errorStack.append(errorMessage)
                        break
            
            else:
                requestList += query_result[:limit]
                    
        return  render(request, 'blog/search_response.html', {'form': form, 'resumeList': requestList, 'errors': errorStack})
        
    elif(request.method == 'POST'):
        form = SearchForm(request.POST)
        return render(request, 'blog/search_response.html', {'form': form})

##Сделать нормално tree - это не bf дерево, это контент ответа на запрос
        
        
def parsingOrigen(request, resume_id):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) 
    
    resume_record = SearchResult.objects.get(id=resume_id)
    absResumeLink = resume_record.url
    
    if(absResumeLink == None):
        return render(request, 'blog/404.html') ## not found 404
    
    if(request.method != "GET"):
        pass
        
    domainName = re.findall(r'\w{0,4}\.?\w+\.ru', absResumeLink)[0]
    domain = Domain.objects.get(domainName=domainName)
    parser = OriginParsing(domain,1,"RESUME")
    parser.generalSchem()
    parser.setErrorTarget()
    linkOrigen = OrigenUrl(domain=domain)
    linkOrigen.setUrlOrPattern(absResumeLink)
    requestOrig = OrigenRequest(domain,linkOrigen)
    requestContent = requestOrig.request()
    
    resumeData = parser.parserResume(requestContent)##parserResume
    
    if(not resumeData):
        form = PasingForm()
    else:
        form = PasingForm(resumeData)
        
    return render(request, 'blog/resume_pars.html', {'form': form, 'resumeBody': requestContent, 'link': absResumeLink}) 

def saveResume(data):
    if(data['command'] == "save"):
        checkPerson = Resume.objects.filter(firstName=data['firstName'], lastName=data['lastName'], middleName=data['middleName'], phone=data['phone'])
        checkPhone = Resume.objects.filter(phone=data['phone'], email=data['email'])
        if((not checkPerson) and (not checkPhone)):
            resumeRecord = Resume.objects.create(firstName=data['firstName'],lastName=data['lastName'],middleName=data['middleName'],gender=data['gender'],phone=data['phone'],email=data['email'],location=data['location'],education=data['education'],experience=data['experience'])#data)
            resumeRecord.save()
            resumeLink = ResumeLink.objects.create(resume=resumeRecord, url=data['link'])
            resumeLink.save()
            status = 'Success'
        else:
            if(checkPerson):
                resumeRecord = checkPerson[0]
            else:
                resumeRecord = checkPhone[0]
            
            resumeLink = ResumeLink.objects.get_or_create(resume=resumeRecord, url=data['link'])
            status = 'Update link'
    else:
        status = "Error no valid operation!"
        
    return JsonResponse({'status': status}) 
        
        
def showeResumes(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) 
        
    if(request.method == 'GET'):
        tableHeader = TableColumnHead.objects.filter(tableName='Resumes')
        resumeRecords = Resume.objects.all()
        for item in resumeRecords:
            item.id = '/resume/link/' + str(item.id)
        return render(request, 'blog/resume_view.html', {'colems': tableHeader, 'resumes': resumeRecords})
        
def showeLink(request, idRecord=0):
    tableHeader = TableColumnHead.objects.filter(tableName='Link')
    resume = Resume.objects.get(id=idRecord)
    ResumeFormSet = modelformset_factory(Resume, form=ResumeForm, extra=0)
    formset = ResumeFormSet(queryset=Resume.objects.filter(id=idRecord))
    #resumeForm = ResumeRecord()
    #resumeForm = modelformset_factory(resume, form=ResumeForm)
    linksResume = ResumeLink.objects.filter(resume=resume)
    
    return render(request, 'blog/link_view.html',{'colems': tableHeader, 'links': linksResume, 'form_resume': formset})
    
def incomingTreatment(request):
    if(request.is_ajax()):
        data = json.loads(request.body.decode())
    if(data['view'] == "showeResumes"):
        pass
    elif(data['view'] == "showeLink"):
        pass
    elif(data['view'] == "parsingOrigen"):
        return saveResume(data)
    return JsonResponse({'status': 'successfully'})
    
    
def searchTask(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) 
    
    table_header = TableColumnHead.objects.filter(tableName='SearchCard')
    search_cards = SearchCard.objects.all()
    
    return render(request, 'blog/search_cards.html',{'colems': table_header, 'search_cards': search_cards})
    
def searchForTask(request, idTask=0):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    search_task = SearchCard.objects.get(id=idTask)
    search_form = SearchForm(search_task.__dict__)
    return render(request, 'blog/search_form.html', {'form' : search_form, 'task_id': idTask})