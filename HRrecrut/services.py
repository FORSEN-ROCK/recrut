import urllib.request as urllib
from urllib.parse   import quote
from bs4 import BeautifulSoup
import lxml
import requests
from .models import SearchObject, VailidValues, SearchSequence, SchemaParsing, Credentials, RequestHeaders, SessionData, CredentialsData
from random import random
from re import findall
#import requests

class LoginServer:
 
    def __init__(self, domain):
        self.domain = domain#Domain.objects.get(domainName=domainName)
        self.authSession = requests.Session()
        self.credentials_id = None
   
    def auth_login(self):
        credentialsData = Credentials.objects.filter(domainName=self.domain).values("id","loginLink")[0]
        self.credentials_id = credentialsData['id']        
        sessinCookies = SessionData.objects.filter(credentials=self.credentials_id).values("cookieName","cookieValue")
        self.authSession.headers = RequestHeaders().get_dict(credentials=self.credentials_id)
        null_cookies = self.check_cookies()
          
        if((not sessinCookies) or null_cookies):
            loginGet = requests.Request("GET", credentialsData['loginLink'])
            preRequest = self.authSession.prepare_request(loginGet)
            loginRequest = self.authSession.send(preRequest)
            
            if(loginRequest.status_code != 200):
                return None
            
            preCookies = self.authSession.cookies.get_dict()
            authData = CredentialsData().get_dict(credentials=self.credentials_id)
            
            for key in authData:
                if(authData[key] == None):
                    authData[key] = preCookies[key]
            
            loginPost = requests.Request("POST", credentialsData['loginLink'], data=authData)
            authPreReguest = self.authSession.prepare_request(loginPost)
            authRequest = self.authSession.send(authPreReguest)
            
            if(authRequest.status_code != 200):
                return None
            
            authCookies = self.authSession.cookies.get_dict()
            credentialsObj = Credentials.objects.get(id=self.credentials_id)
            for key in authCookies:
                SessionData.objects.update_or_create(cookieName=key, cookieValue=authCookies[key], credentials=credentialsObj, defaults={'cookieValue': authCookies[key]},)
                
        else:
            for item in sessinCookies:
                self.authSession.cookies.set(item['cookieName'], item['cookieValue'])   
            
    def auth_out(self):
        SessionData.objects.all().delete()
        ##sessinCookies = SessionData.objects.filter(credentials=self.credentials_id).values("cookieName","cookieValue")
        ##for item in sessinCookies:
            ##SessionData.objects.update_or_create(cookieName=item['cookieName'], cookieValue=item['cookieValue'], credentials=self.credentials_id, defaults={'cookieValue':'NULL'},)
            ##Book.objects.all().delete()
            

    def check_cookies(self):
        sessinCookies = SessionData.objects.filter(credentials=self.credentials_id).values("cookieName","cookieValue")
        for item in sessinCookies:
            if(not item['cookieValue']):
                return True
                
        return False

class SearchingService:


    def choiceSearchLink(self, domainName, SearchMode, ageFrom, ageTo, salaryFrom, salaryTo, gender, text='%s', page='%i'):
        
        age, pay, gen = False, False, False
        if((ageFrom != '' and ageTo != '') or (ageFrom == '' and ageTo !='')):#if(ageFrom or ageTo)
            age = True
            validAge = VailidValues().generateValidDict(domainName, 'age')
        
        if((salaryFrom !='' and salaryTo != '') or (salaryFrom =='' and salaryTo != '')):
            pay = True
            validPay = VailidValues().generateValidDict(domainName, 'pay')
         
        if(gender != None): ## != 'All'
            gen = True
            validGender = VailidValues().generateValidDict(domainNae, 'gender')

        link = SearchObject().determinationLink(domainName, SearchMode, age=age, pay=pay, gender=gen)
        sequence = SearchObject().sequenceParametrs(domainName, SearchMode, age=age, pay=pay, gender=gen)
        baseSequence = SearchSequence().getBaseSequence(domainName)
        searchSchema = link %(eval(sequence))
        
        return searchSchema, baseSequence

        
    def getSearchingResults(self, domain, searchSchema, baseSequence, parSchema, searchText, limit, itemPage, page):
        
        authSession = LoginServer(domain)
        authSession.auth_login()
        
        countRecord = 0##(page - 1) * itemPage ##page = 1 to n
        namberPage = 0
        listOfResumes = []
        while True:
            ##searchSpeak = searchSchema %(namberPage, quote(searchText))#%(quote(searchText), namberPage)
            ##searchSpeak = searchSchema %(quote(searchText), namberPage)
            searchSpeak = searchSchema %(eval(baseSequence))
            ##fil = open('searchSpeak.txt', 'w')
            ##fil.write(searchSpeak)
            connectRequest = requests.Request('GET',searchSpeak)
            connectSession = authSession.authSession.prepare_request(connectRequest)
            content = authSession.authSession.send(connectSession)
            ##connect = urllib.urlopen(searchSpeak)
            ##content = connect.read()
            ##print(content.status_code)
            
            if(content.status_code != 200):
                authSession.auth_out()
                authSession.auth_login()
                
                connectRequest = requests.Request('GET',searchSpeak)
                connectSession = authSession.authSession.prepare_request(connectRequest)
                content = authSession.authSession.send(connectSession)
                
            soupTree = BeautifulSoup(content.text,'html.parser')
            content.close()
            ##connect.close()
            notFound = soupTree.find(parSchema['error']['tagName'], parSchema['error']['attrVal'])
            
            if(notFound == None):
                formPersons = soupTree.findAll(parSchema['bodyResponse']['tagName'], parSchema['bodyResponse']['attrVal'])
                for item in formPersons:
                    ##if(countRecord >= int(limit)):
                    ##   return listOfResumes
                    ##elif ((countRecord >= (page - 1) * itemPage) And (countRecord < page * itemPage)):
                    personMeta = {}
                    jobPay = item.find(parSchema['jobPay']['tagName'], parSchema['jobPay']['attrVal'])
                    #personMeta.setdefault('jobPay', jobPay.get_text())
                    persAge = item.find(parSchema['persAge']['tagName'], parSchema['persAge']['attrVal'])
                    #personMeta.setdefault('persAge', persAge.get_text())
                    jobExp = item.find(parSchema['jobExp']['tagName'], parSchema['jobExp']['attrVal'])
                    if(jobExp != None):
                        personMeta.setdefault('jobExp', jobExp.get_text())
                    link = item.find(parSchema['jobTitle']['tagName'], parSchema['jobTitle']['attrVal'])
                    #personMeta.setdefault('jobTitle', link.get_text())
                    ##if(parSchema['jobTitle']['addOption'] != 'NULL'):
                    if(parSchema['jobTitle']['expression'] != None):
                        ##print(parSchema['jobTitle']['expression'])
                        ##print(eval(parSchema['jobTitle']['expression']))
                        personMeta.setdefault('linkResume', '/search/result/resume/' + eval((parSchema['jobTitle']['expression'])))##eval(parSchema['jobTitle']['addOption']))
                    else:
                        ##'https://hh.ru' + link['href']
                        personMeta.setdefault('linkResume', '/result/resume/' + link['href'])
                        
                    lastJob = item.find(parSchema['lastJob']['tagName'], parSchema['lastJob']['attrVal'])
                    if(lastJob != None):
                        personMeta.setdefault('lastJob', lastJob.get_text())
                    listOfResumes.append(personMeta)
                    countRecord += 1
                    print(countRecord)
                    if(countRecord >= int(limit)):
                        ##print('Exit!!!!')
                        return listOfResumes
            else:
                break
            namberPage += 1
        return listOfResumes    
    
    
    def search(self, searchText, domains, SearchMode='AllText', ageFrom='', ageTo='',salaryFrom='',salaryTo='', gender='', limit='20', itemPage='20', page='1'):
        listOfResume = []
        parsingSchemes = SchemaParsing().generalScheme(domains)
        for domain in parsingSchemes:
            ##authSession = LoginServer(domain)
            ##authSession.auth_login()
            serchScheme, baseSequence = self.choiceSearchLink(domain, SearchMode, ageFrom, ageTo, salaryFrom, salaryTo, gender)
            listOfResume += self.getSearchingResults(domain,serchScheme, baseSequence, parsingSchemes[domain], searchText, limit, itemPage, page)
        return listOfResume
    
    
    
class ResumeParsService:
    ##def choiceParsScheme(self, domainName): 
    
    def getResumeData(self, domain, ResumeURL, parSchema, validSelect):
        ##print('begin----------->')
        try:
            authSession = LoginServer(domain)
            authSession.auth_login()
            ##print('session----->')
            connectRequest = requests.Request('GET',ResumeURL)
            connectSession = authSession.authSession.prepare_request(connectRequest)
            content = authSession.authSession.send(connectSession)
            ##print('getResumeData --------> ', content.status_code)
            
            if(content.status_code != 200):
                authSession.auth_out()
                authSession.auth_login()
                
                connectRequest = requests.Request('GET',ResumeURL)
                connectSession = authSession.authSession.prepare_request(connectRequest)
                content = authSession.authSession.send(connectSession)
                
            #connect = urllib.urlopen(ResumeURL)
            #file = open(str(int(random()*10**15)) + '_' + str(int(random()*10**15)) + '.html', 'bw')
            #content = connect.read()
            #file.write(content)
            #file.close()
            soupTree = BeautifulSoup(content.text,'html.parser')
            resumePage = content.text
            content.close()
            ##connect.close()
        except:
            return None
        else:
            listOfResumes = {}
            notFound = soupTree.find(parSchema['error']['tagName'], parSchema['error']['attrVal'])
            if(notFound == None):
                head = soupTree.find(parSchema['headResume']['tagName'], parSchema['headResume']['attrVal'])
                
                ### Begin Parsing FullName 
                
                if(parSchema['firstName']['tagName'] != None and parSchema['lastName']['tagName'] != None and parSchema['middleName']['tagName'] != None):
                    firstName = head.find(parSchema['firstName']['tagName'], parSchema['firstName']['attrVal'])
                    if(firstName != None):
                        if(parSchema['firstName']['expression'] != None):
                            listOfResumes.setdefault('firstName', eval(parSchema['firstName']['expression']))
                        else:
                            listOfResumes.setdefault('firstName', firstName.get_text())
                    
                    lastName = head.find(parSchema['lastName']['tagName'], parSchema['lastName']['attrVal'])
                    if(lastName != None):
                        if(parSchema['lastName']['expression'] != None):
                            listOfResumes.setdefault('lastName', eval(parSchema['lastName']['expression']))
                        else:
                             listOfResumes.setdefault('lastName', lastName.get_text())
                    
                    middleName = head.find(parSchema['middleName']['tagName'], parSchema['middleName']['attrVal'])
                    if(lastName != None):
                        if(parSchema['middleName']['expression'] != None):
                            listOfResumes.setdefault('middleName', eval(parSchema['middleName']['expression']))
                        else:
                            listOfResumes.setdefault('middleName', middleName.get_text())
                
                ### End Parsing FullName
                
                ### Begin Parsing Gender
                
                gender = head.findAll(parSchema['gender']['tagName'], parSchema['gender']['attrVal'])
                if(gender != None):
                    if(parSchema['gender']['expression'] != None):
                        print(eval(parSchema['gender']['expression']))
                        listOfResumes.setdefault('gender', validSelect[eval(parSchema['gender']['expression'])])
                    else:
                        listOfResumes.setdefault('gender', validSelect[gender[0].get_text()]) 
                ### End Parsing Gender
                
                ### Begin Parsing Phone
                if(parSchema['phone']['tagName'] != None):
                    phone = head.find(parSchema['phone']['tagName'], parSchema['phone']['attrVal'])
                    if(phone != None):
                        listOfResumes.setdefault('phone', ''.join(findall(r'\d+', phone.get_text())))
                
                ### End Parsing Phone
                
                ### Begin Parsing Email
                if(parSchema['email']['tagName']):
                    email = head.find(parSchema['email']['tagName'], parSchema['email']['attrVal'])
                    if(email != None):
                            listOfResumes.setdefault('email', email.get_text())
                
                ### End Parsing Email
                
                ### Begin Parsing Region
                if(parSchema['location']['tagName'] !=None):
                    location = head.findAll(parSchema['location']['tagName'], parSchema['location']['attrVal'])
                    print(location)
                    if(location != None):
                        if(parSchema['location']['expression'] != None):
                            listOfResumes.setdefault('location', eval(parSchema['location']['expression']))
                        else:
                            listOfResumes.setdefault('location', location[0].get_text())
                ### End Parsing Region
                
                ### Begin Parsing Education
                
                if(parSchema['containerEducation']['tagName'] != None):
                    containerEducation = soupTree.findAll(parSchema['containerEducation']['tagName'], parSchema['containerEducation']['attrVal'])
                    if(parSchema['containerEducation']['expression'] != None):
                        containerEducation = eval(parSchema['containerEducation']['expression'])
                    else:
                        containerEducation = containerEducation[0]
                    education = containerEducation.findAll(parSchema['education']['tagName'], parSchema['education']['attrVal'])
                else:
                    education = soupTree.findAll(parSchema['education']['tagName'], parSchema['education']['attrVal'])
                ##print('=============================================',eval(parSchema['education']['expression'])) 
                #print(containerEducation)    
                if(education != None):
                    if(parSchema['education']['expression'] != None):
                        listOfResumes.setdefault('education', eval(parSchema['education']['expression']))
                    else:
                        listOfResumes.setdefault('education', education[0].get_text())
                    
                ### End Parsing Education
                
                ### Begin Parsing ExpJob
                
                if(parSchema['containerExpJob']['tagName'] != None):
                    conteinerExpJob = soupTree.findAll(parSchema['containerExpJob']['tagName'], parSchema['containerExpJob']['attrVal'])
                    if(parSchema['containerExpJob']['expression'] != None):
                        #print('=========================================================================================',len(conteinerExpJob))
                        conteinerExpJob = eval(parSchema['containerExpJob']['expression'])
                    else:
                        #print(conteinerExpJob)
                        conteinerExpJob = conteinerExpJob[0]
                    expJob = conteinerExpJob.findAll(parSchema['expJob']['tagName'], parSchema['expJob']['attrVal'])
                else:
                    expJob = soupTree.find(parSchema['expJob']['tagName'], parSchema['expJob']['attrVal'])
                    
                if(expJob != None):
                    if(parSchema['expJob']['expression'] != None):
                        listOfResumes.setdefault('expJob', eval(parSchema['expJob']['expression']))
                    else:
                        listOfResumes.setdefault('expJob', expJob[0].get_text())
                
                ### End Parsing ExpJob
                
                ### Begin Parsing Last Job
                
                ### End Parsing Last Job
                    
            ##print(listOfResumes)
            return listOfResumes, resumePage
        
    def parsing(self, ResumeURL):
        domain = findall(r'\w{0,4}\.?\w+\.ru', ResumeURL)
        validSelect = VailidValues().generateValidDict(domain[0], 'genderPars')
        ##print(domainName[0])
        ##print(validSelect)
        parseLst = SchemaParsing.objects.filter(domainName=domain, context='RESUME')#.list_values()
        #parsingSchemes = SchemaParsing().generalScheme(domainName, 'RESUME')
        #data, itemPage = self.getResumeData(domainName[0], ResumeURL, parsingSchemes[domainName[0]], validSelect)
        return data, itemPage
        
class ResumeMeta(object):
    def __init__(self,domain,pay=None,**kwargs):
        self.domain = domain
        self.pay = kwargs.get('pay')
        self.age = kwargs.get('age')
        self.jobExp = kwargs.get('jobExp')
        self.jobTitle = kwargs.get('jobTitle')
        self.gender = kwargs.get('gender')
        self.link = kwargs.get('link')              # в системе
        self.origenLink = kwargs.get('origen')      # на сайте источнике
        self.previewLink = kwargs.get('preview')    # предварительный просмотр из системы на источнике
    
    def setAttr(self, attrName, attrVal):
        if(attrName in self.__dict__):
            self.__dict__[attrName] = attrVal
    
    def createLink(self):
        if(not self.origenLink):
            return
        else:
            self.previewLink = self.domain.rootUrl + self.origenLink
            self.link = '/search/result/resume/' + self.previewLink
            
        
class ResumeData(object):
    def __init__(self,first=None,last=None,middle=None,phone=None,email=None,region=None,education=None,expJob=None):
        self.first_name = first
        self.last_name = last
        self.middle_name = middle
        self.phone = phone
        self.email = email
        self.region = region
        self.education = education
        eelf.experience = expJob
    
    def setAttr(self, attrName,attrVal):
        if(attrName in self.__dict__):
            self.__dict__[attrName] = attrVal
        
class OrigenUrl(object):
    def __init__(self,domain=None, url=None):
        self.__domain__ = domain
        self.__url__ = url
        self.__iterNum__ = 0
        self.pattern = None
        
    def setDomain(self, domainName=None):
        if((not self.__url__) and  DomainName):
            self.__domain__ = Domain.objects.get(domainName=domainName)
        if(self.__url__ and (not DomainName)):
            domainName = findall(r'\w{0,4}\.?\w+\.ru', self.__url__)
            self.__domain__ = Domain.objects.get(domainName=domainName)
        else:
            raise TypeError("can not specify Domain and Url at the same time!")
        
    def getDomain(self, isObject=False):
        if(isObject):
            return self.__domain__
        else:
            return self.__domain__.domainName
            
    def setUrlOrPattern(self, url=None, **kvargs):
        if((not url) and self.__domain__):
            #Load Pattern
            self.pattern = SearchObject().getPattern(domain=self.domain,SearchMode=kwargs.get('mode'),ageFrom=kwargs.get('ageFrom'),ageTo=kwargs.get('ageTo'),salaryFrom=kwargs.get('salaryFrom'),salaryTo=kwargs.get('salaryTo'),gender=kwargs.get('gen'))
        if(url and self.__domain__):
            domainName = findall(r'\w{0,4}\.?\w+\.ru', url)
            if(domainName != self.__domain__.domainName):
                raise ValueError("A link can be reinstalled within the same domain")
            else:
                self.__url__ = url
                
    def getUrl(self):
        return self.__url__
    
    def getIterationNum(self):
        if(not self.pattern):
            raise ValueError("Patern link is not defained")
        return self.__iterNum__
        
    def setIterationNum(self, iterationNum=0):
        if(not self.pattern):
            raise ValueError("Pattern link is not defained")
        self.__iterNum__ = iterationNum
        
    def createLink(self, **kwargs):
        if(not self.pattern):
            raise ValueError("Pattern link is not defained")
        
        self.__iterNum__ = self.pattern.startPosition
        listParamtrs = self.pattern.parametrs.split(',')
        for parametr in listParamtrs:
            link = link.replace(parametr, kwargs.get(parametr.lower()))
        
        self.__url__ = link 
    
    def nextOrStartIteration(self):
        if((not self.pattern) and self.__url__):
            raise TypeError("Object url have is not iteration")
        else:
            link = self.__url__.replace(self.pattern.iterator, str(self.__iterNum__))
            self.__iterNum__ += self.pattern.iterStep
        
        return link
            
class OrigenRequest(object):
    def __init__(self,domain=None, linkObj=None):
        self.__domain__ = domain 
        self.link = linkObj
        self.__auth__ = None
   
    def getLink(self, isObject=False):
        if(isObject):
            return self.link
        else:
            return self.link.getUrl()
            
    def setLink(self,domain=None,url=None):
        if(not url and not domain):
            return None
        else:
            self.link = OrigenUrl(domain, url)
    def setLinkObj(self, linkObj):
        if(linkObj):
            self.link = linkObj
            
    def request(self,limit):
        if(not self.__auth__):
           self.__auth__ = LoginServer(self.domain)

        if(self.link.pattern):
            #self.link.createLink(kwargs)
            searchLink = self.link.nextOrStartIteration()
        else:
            searchLink = link.getUrl()
                
        try:
            connectRequest = requests.Request('GET',searchLink)
            connectSession = authSession.authSession.prepare_request(connectRequest)
            content = authSession.authSession.send(connectSession)
            soupTree = BeautifulSoup(content.text,'html.parser')
            content.close()
        except:
            soupTree = None 
        finally:
            return soupTree
        
class OriginParsing(object):
    def __init__(self,domainName,limit,context):
        self.domain = Domain.objects.get(domainName=domainName)
        self.link = OrigenUrl(self.domain)
        self.request = OrigenRequest(self.domain)
        self.context = context
        self.__limit__ = int(limit)
        self.countRecord = 0
        self.__notFound__ = None
        self.__bodyResponse__ = None
        self.__schema__ = None
    
    def createSearchLink(self, **kwargs):
        valList = VailidValues.objects.filter(domain=self.domain, context='SEARCH')
        for item in valList:
            if((kwargs.get('gender') == item.rawValue) and item.criterionName == 'gender'):
                kwargs['gender'] = item.validValue
            if((kwargs.get('ageFrom') == item.rawValue) and item.criterionName == 'ageFrom'):
                kwargs['ageFrom'] = item.validValue
            if((kwargs.get('ageTo') == item.rawValue) and item.criterionName == 'ageTo'):
                 kwargs['ageTo'] = item.validValue
                 
        self.link.setUrlOrPattern(mode=kwargs.get('mode'),ageFrom=kwargs.get('ageFrom'),ageTo=kwargs.get('ageTo'),salaryFrom=kwargs.get('salaryFrom'),salaryTo=kwargs.get('salaryTo'),gen=kwargs.get('gender'))
        self.link.createLink(agefrom=kwargs.get('ageFrom'),ageto=kwargs.get('ageTo'),salaryfrom=kwargs.get('salaryFrom'),salaryto=kwargs.get('salaryTo'),gender=kwargs.get('gender'))
        self.request.setLinkObj(self.link)
        
    def createResumeLink(self, url):
        self.link.setUrlOrPattern(url)
        
    def generalSchem(self):
        prserSchem = []
        parserList = SchemaParsing.objects.filter(domain=self.domain, context=self.context)
        for item in parserList:
            if(item.target == 'error' or item.target == 'bodyResponse'):
                pass
            else:
                row = []
                expression = Expression.objects.filter(SchemaParsing=item)
                row.append(item)
                row.append(expression)
                prserSchem.append(row)
        
        self.__notFound__ = SchemaParsing.objects.get(domain=self.domain, context=self.context, target='error')
        self.__bodyResponse__ = SchemaParsing.objects.get(domain=self.domain, context=self.context, target='bodyResponse')
        self.__schema__ =  prserSchem

    def parsingResume(self):
        resultList = []
        #countResume = 0
        
        #while True:
            #if(self.context == 'RESUME'):
                
            #if(self.context == 'SEARCH'):
            
        notFound = tree.find(self.__notFound__.tagName, {self.__notFound__.attrName : self.__notFound__.attrVal})
        if(not notFound):
            resumes = soupTree.findAll(self.__bodyResponse__.tagName,{self.__bodyResponse__.attrName : self.__bodyResponse__.attrVal})
            for resumeItem in resumes: 
                ##перебор резюме
                resumeRecord = ResumeMeta(self.domain)
                for rowParse in self.__schema__:
                    ##Перебор по строкам схемы парсера
                    for itemOper in rowParse:
                        ##Перебор объектов основных операций
                        if(type(itemOper) is not list):
                            parameter = resumeItem.find(itemOper.tagName, {itemOper.attrName : itemOper.attrVal})
                            parameter = parameter.get_text()
                        else:
                            for extentionOper in itemOper:
                                if(not parameter):
                                    break
                                    
                                if((extentionOper.split) and type(parameter) is str):
                                    parameter = parameter.split(extentionOper.split)
                                    
                                if((extentionOper.shearTo or extentionOper.shearFrom) and type(parameter) is not dict):
                                    parameter = parameter[extentionOper.shearFrom:extentionOper.shearTo]
                                        
                                if((extentionOper.sequence) and type(parameter) is not dict):
                                    parameter = parameter[extentionOper.sequence]
                                        
                                if((extentionOper.regexp) and type(parameter) is str):
                                    parameter = findall(regexp, parameter)

                    resumeRecord.setAttr(itemOper.target, parameter)
                resultList.append(resumeRecord)
                self.countResume +=1
                    
            return resultList
        
        #return resultList
        #parsList = SchemaParsing.objects.filter(domainName=self.domain, context='RESUME')
        #contentHTML = self.
   
#if __name__ == '__main__':
    