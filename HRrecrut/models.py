from django.contrib.auth.models import User
from django.db import models

# Create your models here.
MOSCOW = 'Москва'
SAINT_PETERSBURG = 'Санкт-Петербург'
ROSTOV_ON_DON = 'Ростов на Дону'
KRASNODAR = 'Краснодар'
EKATERINBURG = 'Екатеринбург'
CITY_CHOICES = (
    (MOSCOW, 'Москва'),
    (SAINT_PETERSBURG, 'Санкт-Петербург'),
    (ROSTOV_ON_DON, 'Ростов на Дону'),
    (KRASNODAR, 'Краснодар'),
    (EKATERINBURG, 'Екатеринбург'),
)



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
    #ageFrom = models.CharField("Возраст от", max_length=2)
    #ageTo = models.CharField("Возраст до", max_length=2)
    #salaryFrom = models.CharField("Зарплата от", max_length=7)
    #salaryTo = models.CharField("Зарплата до", max_length=7)
    #gender = models.CharField("Пол", max_length=7,choices=GENDER_CHOICES)
    city = models.CharField("Город", max_length=50, choices=CITY_CHOICES,
                            default=MOSCOW)
    ##experience = models.CharField("Требуемый опыт работы", max_length=7)
    
    class Meta:
        unique_together = (("text", "city"),)

class Resume(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    middle_name = models.CharField("Отчество", max_length=50)
    gender = models.CharField("Пол", max_length=7, choices=GENDER_CHOICES)
    phone = models.CharField("Тел.", max_length=12)
    email = models.CharField("Эл.Почта", max_length=50)
    city = models.CharField("Регион", max_length=100)
    education = models.CharField("Образование", max_length=100)
    experience = models.CharField("Опыт работы", max_length=50)
    user = models.ForeignKey(User, default=1)

    class Meta:
        unique_together = (("first_name","last_name","middle_name","email"),)      
   
class ResumeLink(models.Model):
    url = models.URLField(max_length=100)
    resume = models.ForeignKey(Resume)

    class Meta:    
        unique_together = (("url","resume"),)

class TableColumnHead(models.Model):
    displayName = models.CharField("Отображаемое название", max_length=40)
    fieldName = models.CharField("Поле", max_length=40, null=True)
    tableName = models.CharField("Имя таблицы", max_length=40)


#class UserManager(models.Manager):
        
    
class SearchPattern(models.Model):
    NEVER_MIND = 'all'
    MAN = 'man'
    FEMALE = 'female'
    GENDER_CHOICES = (
        (NEVER_MIND, 'Неважно'),
        (MAN, 'Мужской'),
        (FEMALE, 'Женский'),        
    )
    ALL_TEXT = 'All text'
    IN_TITLE = 'In title'
    KEY_WORDS = 'Key Words'
    MODE_CHOICES = (
        (ALL_TEXT, 'По всему тексту'),
        (IN_TITLE, 'В название резюме'),
        (KEY_WORDS, 'По ключевым словам '),
    )
    '''
    MOSCOW = 'Москва'
    SAINT_PETERSBURG = 'Санкт-Петербург'
    ROSTOV_ON_DON = 'Ростов на Дону'
    KRASNODAR = 'Краснодар'
    EKATERINBURG = 'Екатеринбург'
    CITY_CHOICES = (
        (MOSCOW, 'Москва'),
        (SAINT_PETERSBURG, 'Санкт-Петербург'),
        (ROSTOV_ON_DON, 'Ростов на Дону'),
        (KRASNODAR, 'Краснодар'),
        (EKATERINBURG, 'Екатеринбург'),
    )
    '''
    query_text = models.CharField("Вакансия", max_length=100)
    age_from = models.CharField("Возраст от", max_length=2, null=True)
    age_to = models.CharField("Возраст до", max_length=2, null=True)
    salary_from = models.CharField("Зарплата от", max_length=7, null=True)
    salary_to = models.CharField("Зарплата до", max_length=7, null=True)
    source = models.ForeignKey(Domain)
    user = models.ForeignKey(User)
    #task = models.ForeignKey(SearchTask)
    city = models.CharField("Город", max_length=50, choices=CITY_CHOICES,
                            default=MOSCOW)
    gender = models.CharField("Пол", max_length=7, choices=GENDER_CHOICES,
        default=NEVER_MIND)
    mode = models.CharField("Режим поиска", max_length=10, 
                            choices=MODE_CHOICES,default=ALL_TEXT)

class SearchManager(models.Manager):
    def search(self, query_text, city, mode, 
               source=None, gender=None, experience=None,
               age_from=None, age_to=None, 
               salary_from=None, salary_to=None):
        try:
            query = self.filter(title_resume__contains=query_text, 
                                city=city, mode=mode, ignore=False)
        except:
            pass
        
        if source is not None:
            query = query.filter(source=source)
        if gender is not None:
            query = query.filter(gender=gender)
        if experience is not None:
            query = query.filter(experience=experience)
            
        if(age_from is not None) and (age_to is not None):
            query = query.filter(age__range=(age_from, age_to))
        elif(age_from is not None) and (age_to is None):
            query = query.filter(age__range=(age_from, '100'))
        elif(age_from is None) and (age_to is not None):
            query = query.filter(age_range=('0', age_to))
        
        if(salary_from is not None) and (salary_to is not None):
            query = query.filter(salary__range=(salary_from, salary_to))
        elif(salary_from is not None) and (salary_to is None):
            print(salary_from,salary_to)
            query = query.filter(salary__range=(salary_from, '1000000'))
        elif(salary_from is None) and (salary_to is not None):
            query = query.filter(salary__range=('0', salary_to))
        
        return query
        
    def favorites(self, user):
        return self.filter(elected=user)
        
class SearchResult(models.Model):
    ALL_TEXT = 'All text'
    IN_TITLE = 'In title'
    KEY_WORDS = 'Key Words'
    MODE_CHOICES = (
        (ALL_TEXT, 'По всему тексту'),
        (IN_TITLE, 'В название резюме'),
        (KEY_WORDS, 'По ключевым словам '),
    )
    #search_card = models.ForeignKey(SearchCard, null=True)##
    #pattern = models.ForeignKey(SearchPattern, default=1)
    source = models.ForeignKey(Domain)##
    salary = models.CharField("Ожидаемая Зарплата", max_length=10, 
                            default="По договоренности")
    age = models.CharField("Возраст", max_length=10, null=True)
    experience = models.CharField("Опыт работы", max_length=10, null=True)
    last_job = models.CharField("Последнее место работы", max_length=100, 
                                null=True)
    title_resume = models.CharField("Интересующая должность", max_length=200,
                                    null=True)
    gender = models.CharField("Пол", max_length=7,  null=True)
    city = models.CharField("Город", max_length=50, null=True)
    last_update = models.DateField(
                    "Дата последнего обновление", auto_now=False)
    url = models.URLField("Ссылка", max_length=100)
    #task = models.ForeignKey(SearchTask)
    ignore = models.BooleanField("Игнорировать", default=False)
    track = models.BooleanField("Отслеживать", default=False)
    elected = models.ForeignKey(User, null=True)
    mode = models.CharField("Режим поиска", max_length=10, 
                            choices=MODE_CHOICES,default=ALL_TEXT)
    objects = models.Manager()
    search_objects = SearchManager()
    
    class Meta:    
        unique_together = (("url"),)

class TrackUpdate(models.Model):
    update_date = models.DateField("Последнее обновление", auto_now=True)
    value_sorce = models.CharField("Значение на источнике", max_length=10)
    resume = models.ForeignKey(SearchResult)
        
#class UserSearch(models.Model):
#    pattern = models.ForeignKey(SearchPattern)
#    result = models.ForeignKey(SearchResult)
#    hide = models.BooleanField("Скрыть", default=False)
#    elected = models.BooleanField("Избранный", default=False)
   
        #class ResponsibleWatching(models.Model):
#   searchCard_id = models.ForeignKey(SearchCard)
#   #emplay_id = models.ForeignKey(Emplay)
#   type_cd = models.CharField(max_length=12)

#class Vacancies(models.Model):
#   resume_id = models.ForeignKey(Resume)
#   emplay_id = models.ForeignKey(Emplay)
#   searchCard_id = models.ForeignKey(SearchCard)