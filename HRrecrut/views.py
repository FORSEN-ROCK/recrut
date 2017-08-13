from django.shortcuts import render, redirect
from django.conf import settings
from .forms import AuthorizationForm, SearchForm, PasingForm
from .services import SearchingService, ResumeParsService
from django.contrib.auth import authenticate, login
import datetime

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
        
##def  hello_page(request):
##    return render(request, 'blog/index.html', {})
    
    
##def searchView(request):
##    if( request.method == 'POST'):
##        form = SearchForm(request.POST)
##        if form.is_valid():
##            searchSpeak = form.cleaned_data.get('searchSpeck', None)
##            limitRecords = form.cleaned_data.get('limitRecord', None)
##            radirectString = "/search/query=%s&page=%i" %(searchSpeak,1)
##            recordRespone = getSearchingResults(searchSpeak, limitRecords)
##            ##return render
##            return redirect(radirectString)##, context={'form' : form, 'recordRespone': recordRespone})#, 'recordRespone': recordRespone}) ##HttpResponseRedirect ##recordRespone
##            ##return render(request, 'blog/searchResponse.html', {'form' : form, 'recordRespone': recordRespone})
##    else:
##        form = SearchForm()
##    return render(request, 'blog/search.html', {'form': form})

def searchForm(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        form = SearchForm()
        return render(request, 'blog/searchForm.html', {'form' : form})
    
def responseView(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if(request.GET):
        data = {key : request.GET.get(key) for key in ('query','limit','itemPage','ageTo','ageFrom','salaryTo','salaryFrom', 'gender','sourseList', 'searchMode')}
        #data.setdefault('age_to',request.GET.get('ageTo','none'))
        #data.setdefault('age_to',request.GET.get('ageFrom','none'))
        form = SearchForm(data)
        ##searchOptions = SearchOptions(data['limit'], data['itemPage'])
        response  = SearchingService()
        print('sourseList ===== ',request.GET.get('sourseList'))
        print('data', data['sourseList'].split(','))
        ##recordRespone = getSearchingResults(data['query'], int(data['limit']), data['ageFrom'], data['ageTo'], data['salaryTo'], data['salaryFrom'])
        recordRespone = response.search(data['query'], data['sourseList'].split(','), data['searchMode'], data['ageFrom'], data['ageTo'], data['salaryFrom'], data['salaryTo'], data['gender'], data['limit'])
        
        return render(request, 'blog/searchResponse.html', {'form': form, 'recordRespone' : recordRespone})
    elif(request.POST):
        form = SearchForm(request.POST)
        return render(request, 'blog/searchResponse.html', {'form': form})

        
##def testView(request, parUrl):
##    print('=======>',parUrl)
##    return render(request, 'blog/index.html')
    
  
def resumeScanAndPasing(request, absResumeURL):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        
    print('=======>',absResumeURL)  ##debug
    
    if(absResumeURL == None):
        return render(request, 'blog/404.html') ## not found 404
    
    response = ResumeParsService()
    parseData, resumeBody = response.parsing(absResumeURL)
    form = PasingForm(parseData)
    
    return render(request, 'blog/resumePars.html', {'form' : form, 'resumeURL' : absResumeURL, 'resumeBody' : resumeBody})