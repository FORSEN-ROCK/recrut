import datetime
import re
import json
import math
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, FormView, RedirectView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.forms.models import BaseModelFormSet, modelformset_factory
from .models import *
from .forms import *
from .services import *
from .data_transfer import *

#from .models import Resume, ResumeLink, TableColumnHead
class AuthorizationView(View):
    form_class = AuthorizationForm
    initial = {'key': 'value'}
    template_name = 'Recrut/auth.html'
    redirect_url = '/'
    
    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, { 'form' : form})
        
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        form = self.form_class(initial=self.initial)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(self.redirect_url)
            else:
                return render(request, self.template_name, { 'form' : form, 'message' : u'Учетная запись неактивна, обратитесь к администратору'})
        else:
            return render(request, self.template_name, { 'form' : form, 'message' : u'Введено некорректное имя пользователя или пароль'})

            
class ExitView(View):
    redirect_url = '%s?next=%s'
    
    def get(self, request): 
        logout(request)
        return redirect(self.redirect_url %(settings.LOGIN_URL, request.path))

        
class HomespaceView(LoginRequiredMixin, View):
    template_name = 'Recrut/index.html'
    login_url = '/login/'
    redirect_field_name = ''
    
    def get(self, request):
        date = datetime.datetime.today().strftime('%d-%m-%Y')
        return render(request, self.template_name, {'date' : date})

        
class SearchFormView(LoginRequiredMixin, FormView):
    form_class = SearchForm
    login_url = '/login/'
    redirect_field_name = ''
    template_name = 'Recrut/search_form.html'
 
class FreeSearchView(LoginRequiredMixin, View):
    form_class = SearchForm
    login_url = '/login/'
    redirect_field_name = ''
    template_name = 'Recrut/search_response.html'
    
    def get(self, request, page=1):
        LIMIT = 35
        previous_record = (int(page) - 1) * LIMIT
        next_record = int(page) * LIMIT
        user = request.user
        data = {key : request.GET.get(key) for key in ('query_text',
                                                       'source',
                                                       'city',
                                                       'mode',
                                                       'gender',
                                                       'age_from',
                                                       'age_to',
                                                       'salary_from',
                                                       'salary_to',            
                                                       'page'
                                                       )
        }
        form = self.form_class(initial=data)
        #form = SearchForm(data)
        form.is_valid()
        dataParm = {key.lower() : data[key] for key in data if data[key] != ''}
        response = SearchResult.search_objects.search(
                                query_text=dataParm.get('query_text'),
                                city=dataParm.get('city'),
                                mode=dataParm.get('mode'),
                                source=dataParm.get('source'),
                                gender=dataParm.get('gender'),
                                age_from=dataParm.get('age_from'),
                                age_to=dataParm.get('age_to'),
                                salary_from=dataParm.get('salary_from'),
                                salary_to=dataParm.get('salary_to'))
        for item in response:
            item.id = 'resume/%s' %(item.id)
        response_count = response.count()
        page_count = math.ceil(response_count / LIMIT) + 1
        pages = [{'num': num, 'href': num} for num in range(1, page_count)]
        response = response[previous_record:next_record]
        return render(request, self.template_name, {'form': form,              'resumeList': response, 'pages': pages})
        
        
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
        
    return render(request, 'Recrut/resume_pars.html', {'form': form, 'resumeBody': requestContent, 'link': absResumeLink}) 

    
def saveResume(data):
    if(data['command'] == "save"):
        checkPerson = Resume.objects.filter(firstName=data['firstName'],
                                            lastName=data['lastName'],
                                            middleName=data['middleName'],
                                            phone=data['phone'])
        checkPhone = Resume.objects.filter(phone=data['phone'],
                                           email=data['email'])
        if((not checkPerson) and (not checkPhone)):
            resumeRecord = Resume.objects.create(firstName=data['firstName'],
                                                 lastName=data['lastName'],
                                                 middleName=data['middleName'],
                                                 gender=data['gender'],
                                                 phone=data['phone'],
                                                 email=data['email'],
                                                 location=data['location'],
                                                 education=data['education'],
                                                 experience=data['experience'])#data)
            resumeRecord.save()
            resumeLink = ResumeLink.objects.create(resume=resumeRecord, url=data['link'])
            resumeLink.save()
            '''
            save_candidate(education=data['education'],
                           email=data['email'],
                           experience=data['experience'],
                           first_name=data['firstName'],
                           gender=data['gender'],
                           last_name=data['lastName'],
                           mid_name=data['middleName'],
                           phone=data['phone'],
                           region=data['location'],
                           auto_flg=data['auto_flg'])
            '''
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
        

class ShoweResume(LoginRequiredMixin, ListView):
    model = Resume
    login_url = '/login/'
    redirect_field_name = ''
    context_object_name = 'resumes'
    template_name = 'Recrut/resume_view.html'
    
    def get_queryset(self):
        queryset = self.model.objects.filter(
                        user=self.request.user)
        for item in queryset:
            item.id = '/resume/link/' + str(item.id)
        return queryset
    

class ShoweLinkView(LoginRequiredMixin, View):
    template_name = 'Recrut/link_view.html'
    login_url = '/login/'
    redirect_field_name = ''
    context_object_name = 'resumes'
    form_class = ResumeForm
    model = Resume
    
    def get(self, request, record_id):
        try:
            resume = Resume.objects.get(id=record_id)
        except:
            # return render page 404
            pass
        formset = modelformset_factory(self.model,
                                       form=self.form_class,
                                       extra=0)
        ResumeFormSet = formset(queryset=Resume.objects.filter(id=record_id))
        linksResume = ResumeLink.objects.filter(resume=resume)
        return render(request, self.template_name, {'links': linksResume,             'form_resume': ResumeFormSet})

        
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
    #cards = SearchCard.objects.all()
    search_cards = []
    for item in SearchCard.objects.all():
        item.id = '/search/' + str(item.id)
        search_cards.append(item)
    return render(request, 'blog/search_cards.html',{'colems': table_header, 'search_cards': search_cards})
'''    
def searchForTask(request, idTask=0):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    search_task = SearchCard.objects.get(id=idTask)
    search_form = SearchForm(search_task.__dict__)
    return render(request, 'blog/search_form.html', {'form' : search_form, 'task_id': idTask})
'''


class ShowePattersView(LoginRequiredMixin, View):
    template_name = 'Recrut/search_patterns.html'
    login_url = '/login/'
    redirect_field_name = ''
    
    def get(self, request):
        user = request.user
        patterns = []
        for item in SearchPattern.objects.filter(user=user):
            item.id = '/search/%s' %(item.id)
            patterns.append(item)
        return render(request, self.template_name,{
                     'search_patterns': patterns})


class SearchView(LoginRequiredMixin, View):
    form_class = SearchForm
    login_url = '/login/'
    redirect_field_name = ''
    redirect_url = '/search/%s/result/1'
    
    def get(self, request, pattern_id):
        pattern = SearchPattern.objects.get(id=pattern_id)
        form = self.form_class(initial=pattern.__dict__)
        return redirect(self.redirect_url %(pattern_id))
    
class ResponsSearcheView(LoginRequiredMixin, View):
    form_class = SearchForm
    initial = {'key': 'value'}
    login_url = '/login/'
    redirect_field_name = ''
    template_name = 'Recrut/search_response.html'
    
    def get(self, request, pattern_id, page=1):
        LIMIT = 35
        previous_record = (int(page) - 1) * LIMIT
        next_record = int(page) * LIMIT
        user = request.user    
        pattern = SearchPattern.objects.get(id=pattern_id, user=user)
        form = self.form_class(initial=pattern.__dict__)
        response = SearchResult.search_objects.search(
                                query_text=pattern.query_text,
                                city=pattern.city,
                                mode=pattern.mode,
                                source=pattern.source,
                                gender=pattern.gender,
                                age_from=pattern.age_from,
                                age_to=pattern.age_to,
                                salary_from=pattern.salary_from,
                                salary_to=pattern.salary_to)
        response_count = response.count()
        page_count = math.ceil(response_count / LIMIT) + 1
        pages = [{'num': num, 'href': num} for num in range(1, page_count)]
        response = response[previous_record:next_record]
        return render(request, self.template_name, {'form': form,              'resumeList': response, 'pages': pages})