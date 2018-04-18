import datetime
import re
import json
import math
import time

from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, FormView, RedirectView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.forms.models import BaseModelFormSet, modelformset_factory

from .parser_classes import *
from .models import *
from .forms import *


class BaseException(Exception):
    def __init__(self, message):
        self.message = message


class LoadError(BaseException):
    pass


class SearchKeyError(BaseException):
    pass


class LoginError(BaseException):
    pass


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

    def get(self, request):#, page=1):
        all_text = in_title = included_title = False
        key_word = part_of = False
        org_name = description = position = False

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
        LIMIT = 35
        page = int(data.get('page', 1))
        previous_record = (int(page) - 1) * LIMIT
        next_record = int(page) * LIMIT
        user = request.user

        form = self.form_class(initial=data)
        form.is_valid()
        dataParm = {key.lower() : data[key] for key in data if data[key] != ''}

        if data['source'] == ALL_SOURCE:
            valid_source = None
        else:
            valid_source = data['source']

        if data['mode'] == ALL_TEXT:
            all_text = True
        elif data['mode'] == IN_TITLE_COMP_COIN:
            in_title = True
        elif data['mode'] == IN_TITLE_PART_OF:
            included_title = True
        elif data['mode'] == KEY_WORDS_COMP_COIN:
            key_word = True
        elif data['mode'] == KEY_WORDS_PART_OF:
            key_word = True
            part_of = True
        elif data['mode'] == ORG_NAME_COMP_COIN:
            org_name = True
        elif data['mode'] == ORG_NAME_PART_OF:
            org_name = True
            part_of = True
        elif data['mode'] == IN_EXPERIENCE_DESCRIPTION:
            description = True
        elif data['mode'] == POSITION_NAME_COMP_COIN:
            position = True
        elif data['mode'] == POSITION_NAME_PART_OF:
            position = True
            part_of = True

        if all_text or in_title or included_title:
            response = SearchResult.search_objects.search(
                                query_text=dataParm.get('query_text'),
                                city=dataParm.get('city'),
                                source=valid_source,
                                gender=dataParm.get('gender'),
                                age_from=dataParm.get('age_from'),
                                age_to=dataParm.get('age_to'),
                                salary_from=dataParm.get('salary_from'),
                                salary_to=dataParm.get('salary_to'),
                                all_text=all_text,
                                in_title=in_title,
                                included_title=included_title
            )
        elif key_word:
            key_words_list = KeyWords.search_objects.search(
                                    key_text=dataParm.get('query_text'),
                                    source=valid_source,
                                    gender=dataParm.get('gender'),
                                    city=dataParm.get('city'),
                                    age_from=dataParm.get('age_from'),
                                    age_to=dataParm.get('age_to'),
                                    salary_from=dataParm.get('salary_from'),
                                    salary_to=dataParm.get('salary_to'),
                                    part_of=part_of
            )
            response = [item.resume for item in key_words_list]
        elif org_name or description or position:
            experience_list = Experience.search_objects.search(
                                    query_text=dataParm.get('query_text'),
                                    source=valid_source,
                                    city=dataParm.get('city'),
                                    gender=dataParm.get('gender'),
                                    age_from=dataParm.get('age_from'),
                                    age_to=dataParm.get('age_to'),
                                    salary_from=dataParm.get('salary_from'),
                                    salary_to=dataParm.get('salary_to'),
                                    position=position,
                                    organization_name=org_name,
                                    experience=description,
                                    part_of=part_of
            )
            response = [item.resume for item in experience_list]

        #for item in response:
        #    item.id = 'resume/%s' %(item.id)
        response = [
          {key: getattr(item, key, None) for key in ('id', 'title_resume',
                                                     'age', 'salary',
                                                     'preview',
                                                     'length_of_work',
                                                     'degree_of_education',
                                                     'last_update')}
          for item in response                                    
        ]
        for item_resume in response:
            resume_id = item_resume.get('id')
            try:
                item_experience = Experience.objects.filter(
                                        resume_id=resume_id).order_by('id')
            except IntegrityError:
                item_resume.setdefault('organization_name', None)
                item_resume.setdefault('last_position', None)

            try:
                item_resume.setdefault('organization_name', 
                                       item_experience[0].organization_name)
                item_resume.setdefault('last_position',
                                       item_experience[0].last_position)
            except IndexError:
                item_resume.setdefault('organization_name', None)
                item_resume.setdefault('last_position', None)

            item_resume['id'] = 'resume/%s' %(resume_id)

        response_count = len(response)
        page_count = math.ceil(response_count / LIMIT) + 1
        pages = [{'num': num, 'href': num} for num in range(1, page_count)]
        response = response[previous_record : next_record]
        return render(request, self.template_name, {'form': form,              'resumeList': response, 'pages': pages,
                      'record_count': response_count})


class AuthRecrutSite(View):

    auth_sites = {
        'hh.ru': AuthHh(),
        'www.superjob.ru': AuthSj(),
        'www.avito.ru': AuthAvito(),
        'www.rabota.ru': AuthRabota(),
        'www.farpost.ru': AuthFarpost(),
        'rabotavgorode.ru': AuthRabotavgorode(),
        'www.zarplata.ru': AuthZarplata()

    }

    def _get_cookies(self, domain):
        cookies = SessionData.objects_session.get_cookies(domain)
        return cookies

    def _session_valid(self, session, test_url):
        request = requests.Request("GET", test_url)
        session_request = session.prepare_request(request)
        try:
            responce = session.send(session_request)
        except requests.HTTPError:
            valod = False
        except requests.ConnectionError:
            valid = False
        finally:
            responce.close()

        if responce.status_code != 200:
            valid = False
        else:
            valid = True

        return valid

    def _clear_cookies(self, domain):
        print('Enter>>')
        SessionData.objects_session.clear_cookies(domain)

    def _save_cookies(self, domain, session):
        cookies = session.cookies.get_dict()
        if cookies:
            SessionData.objects_session.save_cookies(domain, cookies)

    def source_cookies(self, site_name):
        current_auth_site = self.auth_sites[site_name]

    def auth_recrut(self, site_name):
        try:
            domain = Domain.objects.get(name=site_name)
        except Domain.DoesNotExist:
            domain = None
        except Domain. MultipleObjectsReturned:
            domain = Domain.objects.filter(name=site_name)[0]

        current_auth_site = self.auth_sites[site_name]
        cookies = self._get_cookies(domain)

        if cookies:
            #session = self._get_session(domain, current_auth_site.headers)
            session = requests.Session()
            session.headers = current_auth_site.headers
            for item in cookies:
                session.cookies.set(item.cookie_name, item.cookie_value)
            session_valid = self._session_valid(session, 
                                                current_auth_site.test_url)

            if not session_valid:
                self._clear_cookies(domain)
                raise LoginError("Session is not valid") 

        else:
            try:
                session = current_auth_site.auth(domain.login, 
                                                 domain.password)
            except AuthError:
                session = None

        if session:
            self._save_cookies(domain, session)

        return session


class ResumeParserView(LoginRequiredMixin, View):
    form_class = ParsingForm##SiebelCandidate
    login_url = '/login/'
    redirect_field_name = ''
    template_name = 'Recrut/resume_pars.html'

    parsers = {
                'hh.ru': SearchHh(),
                'www.superjob.ru': SearchSj(),
                'www.avito.ru': SearchAvito(),
                'www.rabota.ru': SearchRabota(),
                'www.farpost.ru': SearchFarpost(),
                'rabotavgorode.ru': SearchRabotavgorode(),
                'www.zarplata.ru': SearchZarplata()
    }
    auth_view = AuthRecrutSite()

    def get(self, request, resume_id):
        try:
            resume = SearchResult.objects.get(id=resume_id)
        except IntegrityError:
            resume = None
        auth_site = getattr(self, 'auth_view', None)
        parsers = getattr(self, 'parsers', None)

        if resume:
            parser = parsers[resume.source]
            #domain = Domain.objects.get(domainName=resume.source)
            try:
                session = auth_site.auth_recrut(resume.source)
            except LoginError:
                session = auth_site.auth_recrut(resume.source)
            except requests.ConnectionError:
                session = requests.Session()

            resume_list = [{'title_resume': resume.title_resume,
                            'url': resume.url,
                            'last_update': resume.last_update,
                            'source': resume.source,
                            'preview': resume.preview,
                            'search_text': resume.search_text}]
            #session select or create for source site
            resume_update, error_list = parser.search(
                                                    session=session, 
                                                    resume_list=resume_list, 
                                                    update_flad=True
                )
            resume_html = parser.resume_html(session=session,
                                             resume_url=resume.url)
            if len(resume_update) <= 0:
                resume_update = [
                           {
                           'first_name': resume.first_name,
                           'last_name': resume.last_name,
                           'middle_name': resume.middle_name,
                           'phone': resume.phone,
                           'email': resume.email,
                           'city': resume.city,
                           'gender': resume.gender,
                           'length_of_work': resume.length_of_work,
                           'degree_of_education': resume.degree_of_education,
                           }
                ]
            try:
                resume_data = resume_update[0]
            except IndexError:
                resume_data = {}

        else:
            resume_data = {}
            resume_html = None

        ##print(resume_data)
        selected_list = [
                (item.vacancy.id, item.vacancy.job_name) for item in
                SiebelVacancyCandidate.objects.using('siebel').filter(
                    candidate=resume.out_id
                )
        ]        
        choice_list = [(item.id, item.job_name) for item in
                        SiebelVacancy.vacancies.active_vacancies()
                        if (item.id, item.job_name) not in selected_list
        ]
        form = self.form_class(choice_list, selected_list,
                               initial=resume_data)
            #resume_object = SearchResult.create_resume(resume_update)
            #save to siebel

        return render(request, self.template_name, {'form': form,              'resumeBody': resume_html, 'link': resume.url,
                      'source': resume.source})

    def post(self, request, resume_id):
        data = json.loads(request.body.decode())
        siebel_id = gnerate_row_id()
        vacancys_raw = data.get('vacancy')
        status = 'Success'

        if vacancys_raw:
            vacancys = vacancys_raw.split(',')
        else:
            vacancys = None

        try:
            resume_txt = compres_resume(data)
            candidate, created = SiebelCandidate.objects.using(
                                                               'siebel'
            ).get_or_create(first_name=data.get('first_name'),
                            last_name=data.get('last_name'),
                            middle_name=data.get('middle_name'),
                            email=data.get('email'),
                            birth=data.get('birth'),
                            defaults={
                               'id': siebel_id,
                               'first_name': data.get('first_name'),
                               'last_name': data.get('last_name'),
                               'middle_name': data.get('middle_name'),
                               'email': data.get('email'),
                               'birth': data.get('birth'),
                               'education': data.get(
                                                'degree_of_education'),
                               'experience': data.get('length_of_work'),
                               'gender': data.get('gender'),
                               'source': data.get('source'),
                               'auto_flag': data.get('auto_flag'),
                               'region': data.get('city'),
                               'resume_text': resume_txt
                            })
            phone, created = SiebelCommunicationAddres.objects.using(
                                                                'siebel'
            ).get_or_create(addr=data.get('phone'),
                            comm_medium='Phone',
                            candidate=candidate,
                            defaults={'id': siebel_id,
                                      'addr': data.get('phone'),
                                      'comm_medium': 'Phone',
                                      'candidate': candidate})

            resume = SearchResult.objects.get(id=resume_id)
            resume.out_id = candidate.id
            resume.save()

            if vacancys:
                for item_vacancy in vacancys:
                    item_id = gnerate_row_id()
                    try:
                        vacancy = SiebelVacancy.objects.using(
                                                              'siebel'
                        ).get(id=item_vacancy)
                    except IntegrityError:
                        continue
                    try:
                        item_rel = SiebelVacancyCandidate.objects.using(
                                                                'siebel'
                        ).get_or_create(candidate=candidate,
                                        vacancy=vacancy,
                                        defaults={
                                                'id': item_id,
                                                'vacancy': vacancy,
                                                'candidate': candidate})
                    except IntegrityError:
                        continue

        except:
            status = 'error'
        #print(candidate.vacancy.all())
        
        ##form = self.form_class(request)
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
        pages = [{'num': num, 'href': num} for num in 
                 range(1, page_count)]
        response = response[previous_record:next_record]
        return render(request, self.template_name, {'form': form,              'resumeList': response, 'pageso': pages})


class CheckSearchTasksView(View):

    def check(self, debug):
        vacancies = SiebelVacancy.vacancies.active_vacancies()
        search_tasks = SearchKey.objects_load.active_tasks()

        if debug:
            vacancies = vacancies[:5]
            search_tasks = search_tasks[:5]

        if search_tasks:
            for item_task in search_tasks:
                repeat = False
                for item_vacancie in vacancies:
                    if item_task.text == item_vacancie.job_name:
                        repeat = True

                item_task.repeat = repeat
                item_task.save()

        if vacancies:
            for item_vacancie in vacancies:
                SearchKey.objects.get_or_create(
                                text=item_vacancie.job_name,
                                defaults={
                                    'text': item_vacancie.job_name
                                            }
                )

    def check_status(self, debug):
        time.sleep(60)


class DelOldResumeView(View):

    def delete(self, debug):
        inactive_tasks = SearchKey.objects_load.inactive_tasks()

        if debug:
            inactive_tasks = inactive_tasks[:1]

        if len(inactive_tasks) > 0:
            resumes = [] 
            for item_task in inactive_tasks:
                count_record = item_task.count_load
                resumes = SearchResult.objects.filter(
                                            search_text=item_task.text,
                                            out_id=None
                )
                del_record = len(resumes)
                for item_resume in resumes:
                    Education.objects.filter(
                                             resume=item_resume
                    ).delete()
                    Experience.objects.filter(
                                              resume=item_resume
                    ).delete()
                    KeyWords.objects.filter(
                                            resume=item_resume
                    ).delete()

                item_task.count_load = count_record - del_record
                item_task.deleted = True
                item_task.save()
                resumes.delete()


class LoadResumeView(View):
    parsers_list = [
                    SearchHh()
    ]
    auth_view = AuthRecrutSite()

    def load(self, debug, download, update, reload_error):
        parsers = getattr(self, 'parsers_list', None)
        auth_site = getattr(self, 'auth_view', None)

        if not parsers:
            raise LoadError(
                    "List of parsers is empty, loading is not possible"
            )

        if download or update:
            if download:
                search_list = SearchKey.objects_load.load()
            else:
                search_list = SearchKey.objects_load.reload()

            if not search_list:
                raise SearchKeyError("No active update jobs found")

            for source_parser in parsers:
                #source_session = auth_site
                #source_session = requests.Session()
                #source_header = {
                #        item.sectionName: item.body for item in 
                #        RequestHeaders.objects.filter(credentials=1)
                #}
                #source_session.headers = source_header
                source_count = 0
                for search_item in search_list:
                    source_session = auth_site.auth_recrut(
                                                    source_parser.source
                    )
                    load_data, error_data = source_parser.search(
                                               search_str=search_item.text,
                                               session=source_session,
                                               debug_flag=debug
                    )
                    search_item.count_load += len(load_data)
                    search_item.first_load = False

                    if len(search_item.count_load) > 0:
                        search_item.deleted = False

                    search_item.save()
                    resumes = SearchResult.search_objects.create_resume(
                                                                 load_data
                    )
                    education = Education.search_objects.create_education(
                                                                   resumes
                    )
                    experience = Experience.search_objects.create_experience(
                                                                   resumes
                    )
                    key_words = KeyWords.search_objects.create_keys(resumes)
                    check_sum = LoadResumeLog.log_objects.create_log(
                                                                error_data)

        elif reload_error:
            for source_parser in parsers:
                erorr_record = LoadResumeLog.objects.filter(
                                               source=source_parser.source
                )

                if not error_record:
                    raise SearchKeyError("No error doling")

                source_session = auth_site(search_item.source)
                error_list = [
                    {
                        key: getattr(item, key, None) for item in (
                                                            'url',
                                                            'source',
                                                            'last_update',
                                                            'title_resume',
                                                            'review'
                        )
                    } for item in erorr_record
                ]
                load_data, error_data = source_parser.search(
                                               resume_list=error_list,
                                               session=source_session,
                                               debug_flag=debug,
                                               reload_error_flag=reload_error
                )
                resumes = SearchResult.search_objects.create_resume(
                                                                 load_data
                )
                education = Education.search_objects.create_education(
                                                                   resumes
                )
                experience = Experience.search_objects.create_experience(
                                                                   resumes
                )
                key_words = KeyWords.search_objects.create_keys(resumes)
                if len(load_data) >= len(error_data) * 0.9:
                    try:
                        erorr_record.delete()
                    except IntegrityError:
                        continue