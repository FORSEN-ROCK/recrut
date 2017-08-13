import urllib.request as urllib
from urllib.parse   import quote
from bs4 import BeautifulSoup
import lxml
from .models import SearchObject, VailidValues, SearchSequence, SchemaParsing #, OtherAuth
from random import random
from re import findall
#import requests

class SearchingService:


    def choiceSearchLink(self, domainName, SearchMode, ageFrom, ageTo, salaryFrom, salaryTo, gender, text='%s', page='%i'):
        
        age, pay, gen = False, False, False
        if((ageFrom != '' and ageTo != '') or (ageFrom == '' and ageTo !='')):
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

        
    def getSearchingResults(self, searchSchema, baseSequence, parSchema, searchText, limit, itemPage, page):
        countRecord = 0##(page - 1) * itemPage ##page = 1 to n
        namberPage = 0
        listOfResumes = []
        while True:
            ##searchSpeak = searchSchema %(namberPage, quote(searchText))#%(quote(searchText), namberPage)
            ##searchSpeak = searchSchema %(quote(searchText), namberPage)
            searchSpeak = searchSchema %(eval(baseSequence))
            fil = open('searchSpeak.txt', 'w')
            fil.write(searchSpeak)
            connect = urllib.urlopen(searchSpeak)
            content = connect.read()
            soupTree = BeautifulSoup(content,'html.parser')
            connect.close()
            notFound = soupTree.find(parSchema['error']['tagName'], parSchema['error']['attrVal'])
            if(notFound == None):
                formPersons = soupTree.findAll(parSchema['bodyResponse']['tagName'], parSchema['bodyResponse']['attrVal'])
                for item in formPersons:
                    ##if(countRecord >= int(limit)):
                    ##   return listOfResumes
                    ##elif ((countRecord >= (page - 1) * itemPage) And (countRecord < page * itemPage)):
                    personMeta = {}
                    jobPay = item.find(parSchema['jobPay']['tagName'], parSchema['jobPay']['attrVal'])
                    personMeta.setdefault('jobPay', jobPay.get_text())
                    persAge = item.find(parSchema['persAge']['tagName'], parSchema['persAge']['attrVal'])
                    personMeta.setdefault('persAge', persAge.get_text())
                    jobExp = item.find(parSchema['jobExp']['tagName'], parSchema['jobExp']['attrVal'])
                    if(jobExp != None):
                        personMeta.setdefault('jobExp', jobExp.get_text())
                    link = item.find(parSchema['jobTitle']['tagName'], parSchema['jobTitle']['attrVal'])
                    personMeta.setdefault('jobTitle', link.get_text())
                    ##if(parSchema['jobTitle']['addOption'] != 'NULL'):
                    if(parSchema['jobTitle']['expression'] != None):
                        print(parSchema['jobTitle']['expression'])
                        print(eval(parSchema['jobTitle']['expression']))
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
                        print('Exit!!!!')
                        return listOfResumes
            else:
                break
            namberPage += 1
        return listOfResumes    
    
    
    def search(self, searchText, domains, SearchMode='AllText', ageFrom='', ageTo='',salaryFrom='',salaryTo='', gender='', limit='20', itemPage='20', page='1'):
        listOfResume = []
        parsingSchemes = SchemaParsing().generalScheme(domains)
        for domain in parsingSchemes:
            serchScheme, baseSequence = self.choiceSearchLink(domain, SearchMode, ageFrom, ageTo, salaryFrom, salaryTo, gender)
            listOfResume += self.getSearchingResults(serchScheme, baseSequence, parsingSchemes[domain], searchText, limit, itemPage, page)
        return listOfResume
    
    
    
class ResumeParsService:
    ##def choiceParsScheme(self, domainName): 
    
    def getResumeData(self, ResumeURL, parSchema, validSelect):
        try:
            connect = urllib.urlopen(ResumeURL)
            #file = open(str(int(random()*10**15)) + '_' + str(int(random()*10**15)) + '.html', 'bw')
            content = connect.read()
            #file.write(content)
            #file.close()
            soupTree = BeautifulSoup(content,'html.parser')
            resumePage = content
            connect.close()
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
                    
            print(listOfResumes)
            return listOfResumes, resumePage
        
    def parsing(self, ResumeURL):
        domainName = findall(r'\w{0,4}\.?\w+\.ru', ResumeURL)
        validSelect = VailidValues().generateValidDict(domainName[0], 'genderPars')
        #print(domainName[0])
        #print(validSelect)
        parsingSchemes = SchemaParsing().generalScheme(domainName, 'RESUME')
        data, itemPage = self.getResumeData(ResumeURL, parsingSchemes[domainName[0]], validSelect)
        return data, itemPage

   
   
#class LoginServer:
#
#    def getAuthData(self, domainName):
#        data = OtherAuth().getAuthParamers(domainName)
#        authSession = requests.Session()
#        auth = authSession.get(data['link'], auth=(data['otherUserName'],data['otherPass']))
#        if(auth.status_code == 200):
#            sessionCookes = auth.cookies.get_dict()