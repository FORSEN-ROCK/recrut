from django.db import models

# Create your models here.

class Domain(models.Model):
    domainName = models.CharField("Домен",max_length=100)
    descriptions = models.CharField("Описание",max_length=1000, null=True)
    rootUrl = models.CharField("Базовый URL",max_length=150, null=True)
    preview = models.BooleanField("Предварительный просмотр",default=False)
    previewClick = models.BooleanField(default=False)
    itemRecord = models.IntegerField("Число записей на странице",default=20)
    inactive = models.BooleanField(default=False)
    
    class Meta:
        unique_together = (("domainName"),)

class list_of_value(models.Model):
    row_id = models.AutoField(primary_key=True)
    type = models.CharField("Тип", max_length=100)
    lang_id = models.CharField("Язык", max_length=3)
    name = models.CharField("Имя", max_length=100)
    value = models.CharField("Значение", max_length=100)
    
    class Meta:
        unique_together  = (("type", "name"),)
    
        
class SchemaParsing(models.Model):
    target = models.CharField(max_length=100)
    context = models.CharField(max_length=100)
    tagName = models.CharField(max_length=40)
    attrName = models.CharField(max_length=100, null=True)
    attrVal = models.CharField(max_length=200, null=True)
    domain = models.ForeignKey(Domain)
    notAttr = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    parSchemaParsing = models.ForeignKey('SchemaParsing', null=True)
    sequens = models.IntegerField(null=True)
    
    class Meta:
        unique_together  = (("domain","context", "target"),)
    

class Expression(models.Model): 
    split = models.CharField(max_length=2, null=True)
    shearTo = models.IntegerField(null=True)
    shearFrom = models.IntegerField(null=True)
    sequence = models.IntegerField(null=True)
    regexp =  models.CharField(max_length=100, null=True)
    seqOper = models.IntegerField(default=1)
    join = models.CharField(max_length=2, null=True)
    SchemaParsing = models.ForeignKey(SchemaParsing)
    
            
    
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

    def getPattern(self,**kwargs):
        age, pay, gen = False, False, False
        for key in kwargs: #text='%s', page='%i'
            if((key == 'ageTo' or key == 'ageFrom') and (kwargs[key])):
                age = True
            if((key == 'salaryFrom' or key == 'salaryTo') and (kwargs[key])):
                pay = True
            if(key == 'gender' and (kwargs[key] != 'all')):
                gen = True
 
        try:
            urlPattern = SearchObject.objects.get(domain=kwargs['domain'],SearchMode=kwargs['mode'],age=age,pay=pay,gender=gen)
            ##print('---->',SearchObject.objects.get(domain=kwargs['domain'],SearchMode=kwargs['mode'],age=age,pay=pay,gender=gen).link)
        except: 
            urlPattern = SearchObject.objects.get(domain=kwargs['domain'],SearchMode=kwargs['mode'], age=False,pay=False,gender=False)
        
        return urlPattern
      
 
        
        
class VailidValues(models.Model):
    domain = models.ForeignKey(Domain)
    criterionName = models.CharField(max_length=50)
    rawValue = models.CharField(max_length=50, null=True)
    validValue = models.CharField(max_length=50, null=True)
    expression = models.CharField(max_length=100, null=True)
    context = models.CharField(max_length=7)
    
    class Meta:
        unique_together  = (("domain","criterionName", "rawValue", "validValue", "expression","context"),)
    
    
class Credentials(models.Model):
    domain = models.ForeignKey(Domain)
    loginLink = models.CharField(max_length=100)
    testLink = models.CharField(max_length=100,null=True)

    class Meta:
        unique_together = (("domain","loginLink"),)


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

# Choices lists
GENDER_CHOICES = [(item.name,item.value) for item in list_of_value.objects.filter(type='GENDER')]
        

class SearchCard(models.Model):
    text = models.CharField("Вакансия", max_length=100)
    ageFrom = models.CharField("Возраст от", max_length=2)
    ageTo = models.CharField("Возраст до", max_length=2)
    salaryFrom = models.CharField("Зарплата от", max_length=7)
    salaryTo = models.CharField("Зарплата до", max_length=7)
    gender = models.CharField("Пол", max_length=7,choices=GENDER_CHOICES)
    ##experience = models.CharField("Требуемый опыт работы", max_length=7)
    
    class Meta:
        unique_together = (("text", "ageFrom", "ageTo", "salaryFrom", "salaryTo", "gender"),)

class Resume(models.Model):
    firstName = models.CharField("Имя", max_length=50)
    lastName = models.CharField("Фамилия", max_length=50)
    middleName = models.CharField("Отчество", max_length=50)
    gender = models.CharField("Пол", max_length=7, choices=GENDER_CHOICES)
    phone = models.CharField("Тел.", max_length=12)
    email = models.CharField("Эл.Почта", max_length=50)
    location = models.CharField("Регион", max_length=100)
    education = models.CharField("Образование", max_length=100)
    experience = models.CharField("Опыт работы", max_length=50)

    class Meta:
        unique_together = (("firstName","lastName","middleName","email"),)      
   
class ResumeLink(models.Model):
    url = models.URLField(max_length=100)
    resume = models.ForeignKey(Resume)

    class Meta:    
        unique_together = (("url","resume"),)

class TableColumnHead(models.Model):
    displayName = models.CharField("Отображаемое название", max_length=40)
    fieldName = models.CharField("Поле", max_length=40, null=True)
    tableName = models.CharField("Имя таблицы", max_length=40)

class SearchResult(models.Model):
    search_card = models.ForeignKey(SearchCard, null=True)##
    domain = models.ForeignKey(Domain)##
    pay = models.CharField("Ожидаемая Зарплата", max_length=10, default="По договоренности")
    age = models.CharField("Возраст", max_length=10, null=True)
    jobExp = models.CharField("Опыт работы", max_length=10, null=True)
    lastJob = models.CharField("Последнее место работы", max_length=100, null=True)
    jobTitle = models.CharField("Интересующая должность", max_length=200, null=True)
    gender = models.CharField("Пол", max_length=7,  null=True)
    url = models.URLField("Ссылка", max_length=100)
    
    class Meta:    
        unique_together = (("url"),)
    
    
#class ResponsibleWatching(models.Model):
#   searchCard_id = models.ForeignKey(SearchCard)
#   #emplay_id = models.ForeignKey(Emplay)
#   type_cd = models.CharField(max_length=12)

#class Vacancies(models.Model):
#   resume_id = models.ForeignKey(Resume)
#   emplay_id = models.ForeignKey(Emplay)
#   searchCard_id = models.ForeignKey(SearchCard)