from django.db import models

# Create your models here.
class Domain(models.Model):
    domainName = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=1000, null=True)
    rootUrl = models.CharField(max_length=150, null=True)
    preview = models.BooleanField(default=False)
    
    class Meta:
        unique_together = (("domainName"),)

class list_of_value(models.Model):
    row_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    lang_id = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    
    class Meta:
        unique_together  = (("type", "name"),)
    
    def generateSelect(self,type_cd):
        list_choices = list_of_value.objects.filter(type=type_cd).values_list('name','value')
        return list_choices
        
class SchemaParsing(models.Model):
    target = models.CharField(max_length=100)
    context = models.CharField(max_length=100)
    tagName = models.CharField(max_length=40)
    attrName = models.CharField(max_length=100, null=True)
    attrVal = models.CharField(max_length=200, null=True)
    domain = models.ForeignKey(Domain)
    parSchemaParsing = models.ForeignKey('SchemaParsing', null=True)
    
    class Meta:
        unique_together  = (("domain","context", "target"),)
    
    #def generalScheme(self, listDomain=None, context="SEARCH"):
    #    if(listDomain == None):
    #        listDomain = SchemaParsing.objects.distinct().values_list('domainName', flat=True)
    #        
    #    scheme = {key : {} for key in listDomain}    
    #    for item in listDomain:
    #        pasingList = SchemaParsing.objects.filter(domainName=item, context=context).values()
    #        #print(len(pasingList),pasingList)
    #        for parStr in pasingList:
    #            attrVal, target = {}, {}
    #            attrVal.setdefault(parStr['attributeName'],parStr['attributeValue'])
    #            target.setdefault('tagName', parStr['tagName'])
    #            target.setdefault('attrVal', attrVal)
    #            #print(parStr['expression'])
    #            target.setdefault('expression', parStr['expressions'])
    #            scheme[parStr['domainName']].setdefault(parStr['target'], target)
    #    return scheme

class Expression(models.Model): 
    split = models.CharField(max_length=2, null=True)
    shearTo = models.IntegerField(null=True)
    shearFrom = models.IntegerField(null=True)
    sequence = models.IntegerField(null=True)
    regexp =  models.CharField(max_length=100, null=True)
    seqOper = models.IntegerField(default=1)
    join = models.CharField(max_length=2, null=True)
    SchemaParsing = models.ForeignKey(SchemaParsing)
    
    #def get_dict(self,schema_parsing_id=None):
    #    if(schema_parsing_id):
    #        return None
    #    
    #    operations = Expression.objects.filter(SchemaParsing=schema_parsing_id).values("split","shearTo","shearFrom","sequence","regexp")
    #    for oper in operations:
            
    
class SearchObject(models.Model):
    domain = models.ForeignKey(Domain)
    SearchMode = models.CharField(max_length=50)
    age = models.BooleanField(default=False)
    gender = models.BooleanField(default=False)
    pay = models.BooleanField(default=False)
    link = models.CharField(max_length=500)
    parametrs = models.CharField(max_length=150) 
    iterator = models.CharField(max_length=50, default="page")
    iterStep = models.IntegerField(default=1)
    startPosition = models.IntegerField(default=0)
    
    class Meta:
        unique_together  = (("SearchMode", "age", "gender", "pay", "parametrs", "link"),)
 
    #def determinationLink(self, domainName, SearchMode, age=False, gender=False, pay=False):  
    #    searchObject = SearchObject.objects.filter(domainName=domainName, SearchMode=SearchMode, age=age, gender=gender, pay=pay).values_list('link', flat=True)
    #    #print('===> ', searchObject)
    #    return  searchObject[0] 
    #def sequenceParametrs(self, domainName, SearchMode, age=False, gender=False, pay=False):  
    #    sequence = SearchObject.objects.filter(domainName=domainName, SearchMode=SearchMode, age=age, gender=gender, pay=pay).values_list('parametrs', flat=True)
        #print('===> ', sequence)
    #    return  sequence[0] 

    def getPattern(self,**kwargs):
        age, pay, gen = False, False, False
        for key in kwargs: #text='%s', page='%i'
            if((key == 'ageTo' or key == 'ageFrom') and (kwargs[key])):
                age = True
            if((key == 'salaryFrom' or key == 'salaryTo') and (kwargs[key])):
                pay = True
            if(key == 'gender' and kwargs[key]):
                gen = True
 
        try:
            urlPattern = SearchObject.objects.get(domain=kwargs['domain'],SearchMode=kwargs['mode'],age=age,pay=pay,gender=gen)
            print('---->',SearchObject.objects.get(domain=kwargs['domain'],SearchMode=kwargs['mode'],age=age,pay=pay,gender=gen).link)
        except: 
            urlPattern = SearchObject.objects.get(domain=kwargs['domain'],SearchMode=kwargs['mode'], age=False,pay=False,gender=False)
        
        return urlPattern

##     
class SearchExtension(models.Model):
    row_id = models.AutoField(primary_key=True)
    par_row = models.OneToOneField(SearchObject, models.CASCADE, primary_key=False, unique=False)
    baseSequence = models.CharField(max_length=100)
    
    class Meta:
        unique_together  = (("par_row", "baseSequence"),)
        

class SearchSequence(models.Model):
    baseSequence = models.CharField(max_length=100)
    domain = models.ForeignKey(Domain)
    
    class Meta:
        unique_together  = (("baseSequence","domain"),)##,) ##(("par_row", "baseSequence"),) "domainName", "domainName",
        
    #def getBaseSequence(self, domainName):
    #    sequence = SearchSequence.objects.filter(domainName=domainName).values_list('baseSequence', flat=True)
    #    return sequence[0]        
 
        
        
class VailidValues(models.Model):
    domain = models.ForeignKey(Domain)
    criterionName = models.CharField(max_length=50)
    rawValue = models.CharField(max_length=50, null=True)
    validValue = models.CharField(max_length=50, null=True)
    expression = models.CharField(max_length=100, null=True)
    context = models.CharField(max_length=7)
    
    class Meta:
        unique_together  = (("domain","criterionName", "rawValue", "validValue", "expression","context"),)
    
    #def generateValidDict(self, domainName, criterionName):
    #    validValue = {}
    #    listVal = VailidValues.objects.filter(domainName=domainName, criterionName=criterionName).values('rawValue','validValue','expression')
    #    if(len(listVal) == 0):
    #        return None
    #        
    #    for item in listVal:
    #        #print(item)
    #        if(item['rawValue'] != None and item['validValue'] != None and item['expression'] == None):
    #            validValue.setdefault(item['rawValue'], item['validValue'])
    #        elif(item['rawValue'] != None and item['validValue'] == None and item['expression'] != None):
    #            validValue.setdefault(item['rawValue'], eval(item['expression']))
    #        elif(item['rawValue'] == None and item['validValue'] == None and item['expression'] != None):
    #            validValue = eval(item['expression'])
    #        else:
    #            continue
    #    
    #    return validValue
    
class Credentials(models.Model):
    domain = models.ForeignKey(Domain)
    loginLink = models.CharField(max_length=100)
    testLink = models.CharField(max_length=100,null=True)

    class Meta:
        unique_together = (("domain","loginLink"),)

#   def 

class CredentialsData(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100,null=True)
    credentials = models.ForeignKey(Credentials)
    
    class Meta:
       unique_together = (("name","credentials"),)
       
    def get_dict(self, credentials=None):
        if(credentials == None):
            return None
            
        dataRAW = CredentialsData.objects.filter(credentials=credentials).values("name","value")
        dataFormat = {}
        for item in dataRAW:
            dataFormat.setdefault(item['name'], item['value'])
    
        return dataFormat
    
class RequestHeaders(models.Model):
    sectionName = models.CharField(max_length=100)
    body = models.CharField(max_length=200)
    credentials = models.ForeignKey(Credentials)
    
    class Meta:
       unique_together = (("sectionName","credentials"),)

    def get_dict(self, credentials=None):
        if(credentials == None):
            return None
        
        dataRAW = RequestHeaders.objects.filter(credentials=credentials).values("sectionName","body")
        dataFormat = {}
        for item in dataRAW:
            dataFormat.setdefault(item['sectionName'], item['body'])
             
        return dataFormat

class SessionData(models.Model):
    cookieName = models.CharField(max_length=50)
    cookieValue = models.CharField(max_length=100, null=True)
    credentials = models.ForeignKey(Credentials)
   
    class Meta:
        unique_together = (("cookieName","credentials"),)

    def get_dict(self, credentials=None):
        if(credentials == None):
            return None
        
        dataRAW = SessionData.objects.filter(credentials=credentials).values("cookieName","cookieValue")
        dataFormat = {}
        cookies = []
        for item in dataRAW:
            cookies.append(item['cookieName'] + '=' + item['cookieValue'])
        
        dataFormat.setdefaul("Cookie", "; ".join(cookies))
        return dataFormat
        

class SearchCard(models.Model):
   jobTitle = models.CharField(max_length=100)
   ageFrom = models.CharField(max_length=2)
   ageTo = models.CharField(max_length=2)
   payFrom = models.CharField(max_length=7)
   payTo = models.CharField(max_length=7)
   gender = models.CharField(max_length=7)
   expJob = models.CharField(max_length=7)


class Resume(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    expJob = models.CharField(max_length=50)

    class Meta:
        unique_together = (("firstName","lastName","middleName","email"),)
   

class ResumeLink(models.Model):
    url = models.CharField(max_length=100)
    resume = models.ForeignKey(Resume)

    class Meta:    
        unique_together = (("url","resume"),)


#class ResponsibleWatching(models.Model):
#   searchCard_id = models.ForeignKey(SearchCard)
#   #emplay_id = models.ForeignKey(Emplay)
#   type_cd = models.CharField(max_length=12)

#class Vacancies(models.Model):
#   resume_id = models.ForeignKey(Resume)
#   emplay_id = models.ForeignKey(Emplay)
#   searchCard_id = models.ForeignKey(SearchCard)