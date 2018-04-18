import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.utils import IntegrityError

# Create support function.
def gnerate_row_id():
    time = datetime.datetime.utcnow()
    return 'HR-' + str(time.minute) + ':' + str(time.second)

def compres_resume(resume):
    """Tacks resume in format dict
    Returned format string
    """
    data_str = ''
    data_str += 'ФИО: %s %s %s\n' %(resume.get('last_name', ''), 
                                    resume.get('first_name', ''),
                                    resume.get('middle_name', ''))
    data_str += 'Пол: %s\n' %(resume.get('gender', ''))
    data_str += 'Дата рождения: %s\n' %(resume.get('birth', ''))
    data_str += 'Город проживания: %s\n' %(resume.get('city', ''))
    data_str += 'Контактный телефон: %s\n' %(resume.get('phone', ''))
    data_str += 'Электронная почта: %s\n' %(resume.get('email', ''))
    data_str += 'Образование: %s\n' %(resume.get('degree_of_education',
                                                 ''))
    data_str += 'Стаж работы: %s\n' %(resume.get('length_of_work', ''))
    data_str += 'Наличие машины: %s\n' %(resume.get('auto_flag', 'Нет'))
    data_str += 'Источник резюме: %s' %(resume.get('source', ''))
    return data_str


# Create your models here.
MOSCOW = 'Москва'
SAINT_PETERSBURG = 'Санкт-Петербург'
ROSTOV_ON_DON = 'Ростов-на-Дону'
KRASNODAR = 'Краснодар'
EKATERINBURG = 'Екатеринбург'
CITY_CHOICES = (
    (MOSCOW, 'Москва'),
    (SAINT_PETERSBURG, 'Санкт-Петербург'),
    (ROSTOV_ON_DON, 'Ростов-на-Дону'),
    (KRASNODAR, 'Краснодар'),
    (EKATERINBURG, 'Екатеринбург'),
)

ALL_TEXT = 'All text'
IN_TITLE = 'In title'
KEY_WORDS = 'Key Words'
MODE_CHOICES = (
    (ALL_TEXT, 'По всему тексту'),
    (IN_TITLE, 'В название резюме'),
    (KEY_WORDS, 'По ключевым словам '),
)
OPEN = 'Открыта'
RESUMED = 'Возобновлена'

class BaseException(Exception):
    def __init__(self, message):
        self.message = message


class SearchError(BaseException):
    pass


class UpdateError(BaseException):
    pass


class Domain(models.Model):
    name = models.CharField("Домен",max_length=100)
    descriptions = models.CharField("Описание",max_length=1000, null=True)
    #rootUrl = models.CharField("Базовый URL",max_length=150, null=True)
    #preview = models.BooleanField("Предварительный просмотр",default=False)
    #itemRecord = models.IntegerField("Число записей на странице",default=20)
    login_link = models.CharField("Ссылка-авторизации", max_length=100,
                                  null=True)
    test_link = models.CharField("Ссылка-проверки", max_length=100, 
                                 null=True)
    inactive = models.BooleanField("Не активен", default=False)
    login = models.CharField("Имя пользователя", max_length=50, 
                             default="Recrut_plus")
    password = models.CharField("Пароль", max_length=100, 
                                default="Recrut_plus")

    class Meta:
        verbose_name = "Домен"
        verbose_name_plural = "Домены"
        unique_together = (("name"),)


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

        dataRAW = CredentialsData.objects.filter(
                    credentials=credentials).values("name","value")
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

        dataRAW = RequestHeaders.objects.filter(credentials=credentials)
        dataRAW = dataRAW.values("sectionName","body")
        dataFormat = {}
        for item in dataRAW:
            dataFormat.setdefault(item['sectionName'], item['body'])

        return dataFormat


class SessionManager(models.Manager):

    def get_cookies(self, domain):
        try:
            query = self.filter(domain=domain)
        except IntegrityError:
            query = None

        return query

    def clear_cookies(self, domain):
        try:
            query = self.filter(domain=domain)
        except IntegrityError:
            query = None

        if query:
            try:
                delete_count = query.delete()
            except IntegrityError:
                delete_count = (0)
                pass

        return delete_count[0]

    def save_cookies(self, domain, cookies_dict):
        count_creat = 0
        for cookies_name in cookies_dict:
            try:
                object = self.create(cookie_name=cookies_name, 
                                     cookie_value=cookies_dict[cookies_name],
                                     domain=domain)
            except IntegrityError:
                continue
            object.save()
            count_creat += 1

        return count_creat


class SessionData(models.Model):
    cookie_name = models.CharField(max_length=50)
    cookie_value = models.CharField(max_length=100, null=True)
    domain = models.ForeignKey(Domain)

    objects = models.Manager()
    objects_session = SessionManager()


    class Meta:
        unique_together = (("cookie_name", "domain"),)


class SearchKeyManager(models.Manager):

    def _init_counters(self, queryset=None):
        if queryset:
            for item_query in queryset:
                item_query.count_load = 0
                item_query.save()
        else:
            raise IntegrityError("QuerySet is empty")

        return queryset

    def load(self):
        try:
            query = self.filter(first_load=True)
            query = self._init_counters(query)
        except IntegrityError:
            query = None

        return query

    def reload(self):
        try:
            query = self.filter(repeat=True, first_load=False)
            query = self._init_counters(query)
        except IntegrityError:
            query = None

        return query

    def active_tasks(self):
        try:
            query = self.filter(models.Q(repeat=True)|
                                models.Q(first_load=True))
        except IntegrityError:
            query = None

        return query

    def inactive_tasks(self):
        try:
            query = self.filter(deleted=False).filter(
                                                first_load=False
            ).filter(repeat=False)
        except IntegrityError:
            query = None

        return query


class SearchKey(models.Model):

    text = models.CharField("Ключ поиска", max_length=100)
    created = models.DateField("Дата создания", auto_now_add=True)
    repeat = models.BooleanField("Повторяемый", default=False)
    first_load = models.BooleanField("Первая загрузка", default=True)
    reload = models.DateField("Дата перезагрузки", auto_now_add=True)
    count_load = models.IntegerField("Загружено записей", default=0)
    deleted = models.BooleanField("Результаты поиска удалены", 
                                  default=False)

    objects = models.Manager()
    objects_load = SearchKeyManager()


    class Meta:
        verbose_name = "Ключ поиска"
        verbose_name_plural = "Ключи поиска"
        unique_together = (("text"),)


class Resume(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    middle_name = models.CharField("Отчество", max_length=50)
    gender = models.CharField("Пол", max_length=7)#, choices=)
    phone = models.CharField("Тел.", max_length=12)
    email = models.CharField("Эл.Почта", max_length=50)
    city = models.CharField("Регион", max_length=100)
    education = models.CharField("Образование", max_length=100)
    experience = models.CharField("Опыт работы", max_length=50)
    user = models.ForeignKey(User, default=1)

    class Meta:
        unique_together = (
                           ("first_name","last_name","middle_name","email")
        )


class ResumeLink(models.Model):
    url = models.URLField(max_length=100)
    resume = models.ForeignKey(Resume)

    class Meta:
        unique_together = (("url","resume"),)


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


    class Meta:
        verbose_name = "Шаблон поиска"
        verbose_name_plural = "Шаблоны поиска"


class SearchResumeManager(models.Manager):

    def create_resume(self, resumes_list=[]):
        """Method for create resume records
        Takes resumes_list, item resume - dict
        Empty fields is None (key: None)
        """
        for item_resume in resumes_list:
            update_value = {
                key: item_resume[key] for key in ('first_name',
                                                  'last_name', 
                                                  'middle_name', 
                                                  'phone', 
                                                  'email', 
                                                  'last_update')
            }
            update_value.setdefault('update_record', 
                                datetime.datetime.utcnow())
            try:
                object, created = self.update_or_create(
                    title_resume=item_resume['title_resume'],
                    first_name=item_resume['first_name'],
                    last_name=item_resume['last_name'],
                    middle_name=item_resume['middle_name'],
                    phone=item_resume['phone'],
                    email=item_resume['email'],
                    gender=item_resume['gender'],
                    age=item_resume['age'],
                    salary=item_resume['salary'],
                    length_of_work=item_resume['length_of_work'],
                    degree_of_education=item_resume['degree_of_education'],
                    city=item_resume['city'],
                    last_update=item_resume['last_update'],
                    source=item_resume['source'],
                    url=item_resume['url'],
                    preview=item_resume['preview'],
                    search_text=item_resume['search_text'],
                    defaults=update_value
                )
            except IntegrityError:
                continue
            object.save()

            if created:
                item_resume.setdefault('object', object)
            else:
                item_resume.setdefault('object', None)

        return resumes_list

    def search(self, query_text, city, 
               source=None, gender=None, length_of_work=None,
               age_from=None, age_to=None, degree_of_education=None, 
               salary_from=None, salary_to=None, all_text=True, 
               in_title=False, included_title=False):

        if all_text and in_title and included_title:
            error = SearchError('the search conditions are not defined,' + 
                                'set one flag to true')
            raise error

        try:
            if all_text:
                query = self.filter(search_text=query_text, ignore=False)

            if in_title:
                query = self.filter(title_resume=query_text, ignore=False)

            if included_title:
                query = self.filter(title_resume__contains=query_text,
                                    ignore=False)
        except DatabaseError:
            pass

        if source:
            query = query.filter(source=source)
        if gender:
            query = query.filter(gender=gender)
        if length_of_work:
            query = query.filter(length_of_work=length_of_work)
        if degree_of_education:
            query = query.filter(degree_of_education=degree_of_education)
        if city:
            query = query.filter(city=city)

        if age_from and age_to:
            query = query.filter(age__range=(age_from, age_to))
        elif age_from and not age_to:
            query = query.filter(age__gte=age_from)
        elif not age_from and age_to:
            query = query.filter(age__lte=age_to)

        if salary_from and salary_to:
            query = query.filter(salary__range=(salary_from, salary_to))
        elif salary_from and not salary_to:
            query = query.filter(salary__gte=salary_from)
        elif not salary_from and salary_to:
            query = query.filter(salary__lte=salary_to)

        return query

    def favorites(self, user):
        return self.filter(elected=user)


class SearchResult(models.Model):

    created = models.DateField("Дата создания", auto_now=True)
    update_record = models.DateField("Дата обновления", auto_now=True)
    title_resume = models.CharField("Заголовок резюме", max_length=200,
                                    null=True)
    first_name = models.CharField("Имя", max_length=50, null=True)
    last_name = models.CharField("Фамилия", max_length=50, null=True)
    middle_name = models.CharField("Отчество", max_length=50, null=True)
    phone = models.CharField("Телефон", max_length=11, null=True)
    email = models.CharField("Эл.Почта", max_length=50, null=True)
    gender = models.CharField("Пол", max_length=7,  null=True)
    age = models.IntegerField("Возраст", null=True)
    birth = models.DateField("Дата рождения", null=True)
    salary = models.IntegerField("Ожидаемая Зарплата", null=True)
    length_of_work = models.CharField("Стаж работы", max_length=30, 
                                      null=True)
    degree_of_education = models.CharField("Тип образования", max_length=50,
                                            null=True)
    city = models.CharField("Город", max_length=100, null=True)
    last_update = models.CharField(
                            "Дата последнего обновление", max_length=50
    )
    source = models.CharField("Источник", max_length=20)##
    url = models.URLField("Ссылка", max_length=100)
    search_text = models.CharField("Ключ поиска", max_length=200, 
                                   default="Python")
    preview = models.BooleanField("Предварительный просмотор", default=False)
    #task = models.ForeignKey(SearchTask)
    ignore = models.BooleanField("Игнорировать", default=False)
    track = models.BooleanField("Отслеживать", default=False)
    elected = models.ForeignKey(User, null=True)
    out_id = models.CharField(null=True, max_length=15)

    objects = models.Manager()
    search_objects = SearchResumeManager()


    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"
        unique_together = (("url"),)


class EducationSearchManager(models.Manager):

    def create_education(self, resumes_list):
        count = 0
        for item_resume in resumes_list:
            resume = item_resume.get('object')
            education_list = item_resume.get('education')

            if not resume or not education_list:
                continue

            for education in education_list:
                try:
                    object = self.create(
                                 resume=resume,
                                 year=education['education_year'],
                                 name=education['education_name'],
                                 profession=education['education_profession'],
                                 source=item_resume['source']
                    )
                except IntegrityError:
                    continue
                object.save()
                count += 1

        return count


    def search(self, year=None, name=None, profession=None, source=None,
               complete_coincidence=False):
        try:

            if source:
                query = self.filter(source=source)
            else:
                query = self.all()

        except:
            pass

        if year:
            query = query.filter(year=year)

        if name:

            if complete_coincidence:
                query = query.filter(name=name)
            else:
                query = query.filter(name__contains=name)

        if profession:

            if complete_coincidence:
                query = query.filter(profession=profession)
            else:
                query = query.filter(profession__contains=profession)

        if query.ordered:
            query.order_by()

        return query#.distinct('resume')


class Education(models.Model):
    resume = models.ForeignKey(SearchResult)
    year = models.CharField("Год окончания", max_length=4)
    name = models.CharField("Учебное заведение", max_length=150)
    profession = models.CharField("Профессия", max_length=150)
    source = models.CharField("Источник", max_length=20)

    objects = models.Manager()
    search_objects = EducationSearchManager()


    class Meta:
        verbose_name = "Образование"
        verbose_name_plural = "Образование"


class ExperienceSearchManager(models.Manager):

    def create_experience(self, resumes_list):
        count = 0
        for item_resume in resumes_list:
            resume = item_resume.get('object')
            experience_list = item_resume.get('experience')

            if not resume or not experience_list:
                continue

            for experience in experience_list:
                try:
                    object = self.create(
                        resume=resume,
                        experience_period=experience['experience_period'],
                        last_position=experience['last_position'],
                        organization_name=experience['organization_name'],
                        experience_text=experience['experience_text'],
                        source=item_resume['source'],
                        gender=item_resume['gender'],
                        city=item_resume['city'],
                        age=item_resume['age'],
                        salary=item_resume['salary']
                    )
                except IntegrityError:
                    continue
                object.save()
                count += 1

        return count

    def search(self, query_text, source=None, gender=None, city=None,
               age_from=None, age_to=None, salary_from=None, salary_to=None,
               period=False, position=True, organization_name=False,
               experience=False, part_of=False):
        try:

            if source:
                query = self.filter(source=source)
            else:
                query = self.all()
        except IntegrityError:
            query = None

        if not query:
            raise SearchError("Search is failed")

        if period and position and organization_name and experience:
            raise SearchError(
                "Search is failed, search parameters are not defined"
            )

        if position:

            if part_of:
                query = query.filter(last_position__contains=query_text)
            else:
                query = query.filter(last_position=query_text)

        if organization_name:

            if part_of:
                query = query.filter(
                            organization_name__contains=query_text
                )
            else:
                query = query.filter(
                                organization_name=query_text
                )

        if experience:
            query = query.filter(
                                experience_text__contains=query_text
            )

        if period:
            query = query.filter(experience_period__contains=query_text)

        if gender:
            query = query.filter(gender=gender)

        if city:
            query = query.filter(city=city)

        if age_from and age_to:
            query = query.filter(age__range=(age_from, age_to))
        elif age_from and not age_to:
            query = query.filter(age__gte=age_from)
        elif not age_from and age_to:
            query = query.filter(age__lte=age_to)

        if salary_from and salary_to:
            query = query.filter(salary__range=(salary_from, salary_to))
        elif salary_from and not salary_to:
            query = query.filter(salary__gte=salary_from)
        elif not salary_from and salary_to:
            query = query.filter(salary__lte=salary_to)

        if query.ordered:
            query.order_by()

        return query#.distinct('resume')


class Experience(models.Model):
    resume = models.ForeignKey(SearchResult)
    experience_period = models.CharField("Период", max_length=20)
    last_position = models.CharField("Позиция", max_length=150)
    organization_name = models.CharField("Организация", max_length=150)
    experience_text = models.CharField("Описание", max_length=500)
    source = models.CharField("Источник", max_length=20)
    gender = models.CharField("Пол", max_length=7,  null=True)
    age = models.IntegerField("Возраст", null=True)
    salary = models.IntegerField("Ожидаемая Зарплата", null=True)
    city = models.CharField("Город", max_length=100, null=True)

    objects = models.Manager()
    search_objects = ExperienceSearchManager()


    class Meta:
        verbose_name = "Опыт работы"
        verbose_name_plural = "Опыт работы"


class KeyWordsSearchManager(models.Manager):

    def create_keys(self, resumes_list):
        count = 0
        for item_resume in resumes_list:
            resume = item_resume.get('object')
            key_word_list = item_resume.get('key_words')

            if not resume or not key_word_list:
                continue

            for key_word in key_word_list:
                try:
                    object = self.create(resume=resume,
                                         key_text=key_word,
                                         source=item_resume['source'],
                                         gender=item_resume['gender'],
                                         age=item_resume['age'],
                                         salary=item_resume['salary'],
                                         city=item_resume['city'])
                except IntegrityError:
                    continue
                object.save()
                count += 1

        return count

    def search(self, key_text, source=None, gender=None,
               city=None, age_from=None, age_to=None, salary_from=None,
               salary_to=None, part_of=True): 
        try:

            if source:
                query = self.filter(source=source)
            else:
                query = self.all()

        except IntegrityError:
            query = None

        if not query:
            raise SearchError("Search is failed")

        if part_of:
            query = query.filter(key_text__contains=key_text)
        else:
            query = query.filter(key_text=key_text)

        if gender:
            query = query.filter(gender=gender)

        if city:
            query = query.filter(city=city)

        if age_from and age_to:
            query = query.filter(age__range=(age_from, age_to))
        elif age_from and not age_to:
            query = query.filter(age__gte=age_from)
        elif not age_from and age_to:
            query = query.filter(age__lte=age_to)

        if salary_from and salary_to:
            query = query.filter(salary__range=(salary_from, salary_to))
        elif salary_from and not salary_to:
            query = query.filter(salary__gte=salary_from)
        elif not salary_from and salary_to:
            query = query.filter(salary__lte=salary_to)

        if query.ordered:
            query.order_by()

        return query##.distinct('resume')


class KeyWords(models.Model):
    resume = models.ForeignKey(SearchResult)
    key_text = models.CharField("Ключевое слово", max_length=50)
    source = models.CharField("Источник", max_length=20)
    gender = models.CharField("Пол", max_length=7,  null=True)
    age = models.IntegerField("Возраст", null=True)
    salary = models.IntegerField("Ожидаемая Зарплата", null=True)
    city = models.CharField("Город", max_length=100, null=True)

    objects = models.Manager()
    search_objects = KeyWordsSearchManager()


    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"


class TrackUpdate(models.Model):
    update_date = models.DateField("Последнее обновление", auto_now=True)
    value_sorce = models.CharField("Значение на источнике", max_length=10)
    resume = models.ForeignKey(SearchResult)


class LoadResumeLogManager(models.Manager):

    def create_log(self, error_list):
        """Takes error_list in format: {
            'title_resume':val,
            'last_update': val,
            'url': val,
            'review': <True/False>,
            'source': val,
        }
        Returned count created record    
        """
        count = 0
        for error in error_list:
            try:
                object = self.create(
                                     title_resume=error['title_resume'],
                                     last_update=error['last_update'],
                                     url=error['url'],
                                     review=error['review'],
                                     source=error['source']
                                    )
            except IntegrityError:
                continue
            object.save()
            count += 1
        return count


class LoadResumeLog(models.Model):
    """Save a failed resume
    """
    title_resume = models.CharField("Заголовок резюме", max_length=200,
                                    null=True)
    last_update = models.CharField(
                            "Дата последнего обновление", max_length=50
    )
    url = models.URLField("Ссылка", max_length=100)
    review = models.BooleanField("Предварительный просмотор", 
                                 default=False)
    source = models.CharField("Источник", max_length=20)
    reload = models.BooleanField("Перезагружен", default=False)

    objects = models.Manager()
    log_objects = LoadResumeLogManager()


    class Meta:
        verbose_name = 'Статусы загрузок'
        verbose_name_plural = 'Статус загрузки'
        unique_together = (("url"),)


##############################SIEBEL###################################
class VacanciesManager(models.Manager):

    def active_vacancies(self):
        return self.using('siebel').filter(models.Q(status=OPEN)|
                                           models.Q(status=RESUMED))


class SiebelCandidate(models.Model):
    id = models.CharField(db_column='row_id', max_length=15,
                          verbose_name='id', primary_key=True)
    created = models.DateField(db_column='created',
                               verbose_name="Дата создания",
                               auto_now_add=True)
    created_by = models.CharField(db_column='created_by', 
                                  max_length=15,
                                  verbose_name='Created by', 
                                  default='0-1')
    last_upd = models.DateField(db_column='last_upd',
                                verbose_name='Дата обновления',
                                auto_now_add=True)
    last_upd_by = models.CharField(db_column='last_upd_by',
                                   max_length=15,
                                   default='0-1')
    #db_last_upd = models.DateField(db_column='db_last_upd',
    #                               auto_now_add=True)
    first_name = models.CharField(db_column='first_name',max_length=50,
                                  verbose_name='Имя',null=True)
    last_name = models.CharField(db_column='last_name', max_length=50,
                                 verbose_name='Фамилия', null=True)
    middle_name = models.CharField(db_column='mid_name', max_length=50,
                                   verbose_name='Отчество', null=True)
    phone = models.CharField(db_column='phone', max_length=50,
                             verbose_name='Телефон', null=True)
    education = models.CharField(db_column='education', max_length=50,
                                 verbose_name='Образование', null=True)
    email = models.CharField(db_column='email', max_length=50,
                             verbose_name='E-mail',null=True)
    experience = models.CharField(db_column='experience', max_length=50,
                                  verbose_name='Опыт работы', null=True)
    gender = models.CharField(db_column='gender', max_length=10,
                              verbose_name='Пол', null=True)
    source = models.CharField(db_column='source', max_length=50,
                              verbose_name='Источник', null=True)
    auto_flag = models.CharField(db_column='auto_flg', max_length=1,
                                verbose_name='Есть машина', default='N')
    resume_text = models.TextField(db_column='resume_text', null=True,
                                   verbose_name='Текст резюмэ')
    region = models.CharField(db_column='region', max_length=50,
                              verbose_name='Регион', null=True)
    birth = models.DateField(db_column='birth_date', null=True,
                               verbose_name="Дата рождения")
    #position = models.CharField(db_column='position', max_length=50,
    #                            verbose_name='Позиция', null=True)
    #job_vacancy = models.CharField(db_column='job_vacancy', null=True
    #                               max_length=50, verbose_name='')
    vacancy = models.ManyToManyField('SiebelVacancy', 
                                     through='SiebelVacancyCandidate')

    objects = models.Manager()


    class Meta:
        db_table = 'cx_candidate'
        db_tablespace = 'data'
        verbose_name = 'Кандидата в CRM'
        verbose_name_plural = 'Кандидаты в CRM'
        managed = False


class SiebelVacancy(models.Model):
    id = models.CharField(db_column='row_id', max_length=15,
                          primary_key=True)
    created = models.DateField(db_column='created',
                               verbose_name="Дата создания",
                               auto_now_add=True)
    created_by = models.CharField(db_column='created_by', 
                                  max_length=15,
                                  verbose_name='Создатель', 
                                  default='0-1')
    last_upd = models.DateField(db_column='last_upd',
                                verbose_name='Дата обновления',
                                auto_now_add=True)
    last_upd_by = models.CharField(db_column='last_upd_by',
                                   max_length=15,
                                   verbose_name='Обновил',
                                   default='0-1')
    #db_last_upd = models.DateField(db_column='db_last_upd')
    status_date = models.DateField(db_column='status_date')
    job_name = models.CharField(db_column='job_name', max_length=100,
                                null=True, 
                                verbose_name='Должность')
    status = models.CharField(db_column='status_cd', max_length=50,
                              verbose_name='Статус вакансии', null=True)

    objects = models.Manager()
    vacancies = VacanciesManager()
    


    class Meta:
        db_table = 'cx_vacancy'
        db_tablespace = 'data'
        verbose_name = 'Вакансию в CRM'
        verbose_name_plural = 'Вакансии из CRM'
        managed = False


class SiebelVacancyCandidate(models.Model):
    id = models.CharField(db_column='row_id', max_length=15,
                          primary_key=True)
    created = models.DateField(db_column='created',
                               verbose_name="Дата создания",
                               auto_now_add=True)
    created_by = models.CharField(db_column='created_by', 
                                  max_length=15,
                                  verbose_name='Создатель', 
                                  default='0-1')
    last_upd = models.DateField(db_column='last_upd',
                                verbose_name='Дата обновления',
                                auto_now_add=True)
    last_upd_by = models.CharField(db_column='last_upd_by',
                                   max_length=15,
                                   verbose_name='Обновил',
                                   default='0-1')
    candidate = models.ForeignKey(SiebelCandidate, 
                                  db_column='candidate_id')
    vacancy = models.ForeignKey(SiebelVacancy, db_column='vacancy_id')

    objects = models.Manager()


    class Meta:
        db_table = 'cx_vac_cand'
        db_tablespace = 'data'
        managed = False


class SiebelCommunicationAddres(models.Model):
    id = models.CharField(db_column='row_id', max_length=15,
                          primary_key=True)
    created = models.DateField(db_column='created',
                               verbose_name="Дата создания",
                               auto_now_add=True)
    created_by = models.CharField(db_column='created_by', 
                                  max_length=15,
                                  verbose_name='Создатель', 
                                  default='0-1')
    last_upd = models.DateField(db_column='last_upd',
                                verbose_name='Дата обновления',
                                auto_now_add=True)
    last_upd_by = models.CharField(db_column='last_upd_by',
                                   max_length=15,
                                   verbose_name='Обновил',
                                   default='0-1')
    addr = models.CharField(db_column='addr', max_length=100,
                            verbose_name='Контактый телефон')
    comm_medium = models.CharField(db_column='comm_medium_cd',
                                   max_length=30, verbose_name='Тип',
                                   default='Phone')
    candidate = models.ForeignKey(SiebelCandidate, db_column='per_id')

    objects = models.Manager()


    class Meta:
        db_table = 's_per_comm_addr'
        db_tablespace = 'data'
        verbose_name = 'Телефон в CRM'
        verbose_name_plural = 'Телефоны из CRM'
        managed = False