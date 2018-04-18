from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from django.forms.widgets import PasswordInput, RadioSelect, CheckboxSelectMultiple, Select, SelectMultiple, MultiWidget
from django.contrib.admin import widgets

from .models import  SiebelCandidate, SiebelVacancy
from .widgets import ManyToManyWidget, CalendarWidget


#Custom field
class ManyToManyField(forms.MultiValueField):
    def __init__(self, choice=[], selected=[], *args, **kwargs):
        list_fields = [forms.MultipleChoiceField(choices=choice),
                       forms.MultipleChoiceField(choices=selected)
                       ]
        super(ManyToManyField, self).__init__(
                        list_fields, 
                        widget=ManyToManyWidget(choice, selected),
                        *args,
                        **kwargs
        )


#Choices List
NEVER_MIND = None
MAN = 'М'
FEMALE = 'Ж'
GENDER_CHOICES = (
   (NEVER_MIND, 'Неважно'),
   (MAN, 'Мужской'),
   (FEMALE, 'Женский'),        
)

ALL_TEXT = 'All text'
IN_TITLE_COMP_COIN = 'In title, complete coincidence'
IN_TITLE_PART_OF = 'In title is part of'
KEY_WORDS_COMP_COIN = 'Key Words, complete coincidence'
KEY_WORDS_PART_OF = 'Key Words part of'
ORG_NAME_COMP_COIN = 'Organization name, complete coincidence'
ORG_NAME_PART_OF  = 'Organization name part of'
IN_EXPERIENCE_DESCRIPTION = 'In experience descriptions'
POSITION_NAME_COMP_COIN = 'Last position name, complete coincidence'
POSITION_NAME_PART_OF = 'Last position name part of'
MODE_CHOICES = (
   (ALL_TEXT, 'По всему тексту'),
   (IN_TITLE_COMP_COIN, 'В название резюме, полное совпадение'),
   (IN_TITLE_PART_OF, 'В название резюме, входит в состав'),
   (KEY_WORDS_COMP_COIN, 'По ключевым словам, полное совпадение'),
   (KEY_WORDS_PART_OF, 'По ключевым словам, входит в состав'),
   (ORG_NAME_COMP_COIN, 'По организации, полное совпадение'),
   (ORG_NAME_PART_OF, 'По организации, входит в состав'),
   (IN_EXPERIENCE_DESCRIPTION, 'В описание опыта работы'),
   (POSITION_NAME_COMP_COIN, 'В названии должности, полное совпадение'),
   (POSITION_NAME_PART_OF, 'В названии должности, входит в состав')
)
MOSCOW = 'Москва'
SAINT_PETERSBURG = 'Санкт-Петербург'
ROSTOV_ON_DON = 'Ростов-на-Дону'
KRASNODAR = 'Краснодар'
EKATERINBURG = 'Екатеринбург'
KALININGRAD = 'Калининград'
CITY_CHOICES = (
    (MOSCOW, 'Москва'),
    (SAINT_PETERSBURG, 'Санкт-Петербург'),
    (ROSTOV_ON_DON, 'Ростов-на-Дону'),
    (KRASNODAR, 'Краснодар'),
    (EKATERINBURG, 'Екатеринбург'),
    (KALININGRAD, 'Калининград')
)
ALL_SOURCE = 'Искать по всем'
HEAD_HANTER = 'hh.ru'
SUPER_JOB = 'www.superjob.ru'
RABOTA_RU = 'www.rabota.ru'
AVITO = 'www.avito.ru'
RABOTA = 'www.rabota.ru'
FORPOST = 'www.farpost.ru'
RABOTAVGORODE = 'rabotavgorode.ru'
ZARPLATA = 'www.zarplata.ru'
SOURCE_CHOICES = (
    (ALL_SOURCE, 'Искать по всем'),
    (HEAD_HANTER, 'hh.ru'),
    (SUPER_JOB, 'superjob.ru'),
    (RABOTA_RU, 'rabota.ru'),
    (AVITO, 'avito.ru'),
    (RABOTA, 'rabota.ru'),
    (FORPOST, 'farpost.ru'),
    (RABOTAVGORODE, 'rabotavgorode.ru'),
    (ZARPLATA,'zarplata.ru')
)


class ResumeRecord(forms.Form):
    firstName = forms.CharField(label="Имя" ,max_length=50)
    lastName = forms.CharField(label="Фамилия" ,max_length=50)
    middleName = forms.CharField(label="Отчество" ,max_length=50)
    gender = forms.ChoiceField(label="Пол" ,widget=Select, choices=                           GENDER_CHOICES)
    phone = forms.CharField(label="Телефон" ,max_length=12)
    email = forms.EmailField(label="E-mail" ,required=True)
    location = forms.CharField(label="Регион" ,max_length=100)
    education = forms.CharField(label="Образование" ,max_length=100)
    experience = forms.CharField(label="Опыт работы" ,max_length=50)


class AuthorizationForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", max_length=60, required=True)
    password = forms.CharField(label="Пароль", max_length=32, widget=PasswordInput, required=True)
'''
class SearchForm(forms.Form):
    text = forms.CharField(label=False, max_length=100, required=True)
    limit = forms.CharField(label="Число записей с источника:", max_length=30,                        required=False)
    itemPage = forms.CharField(label="Число записей на странице:", 
                               max_length=3, required=False)
    ageFrom = forms.CharField(label="Возраст от:", max_length=2, 
                              required=False)
    ageTo = forms.CharField(label="Возраст до:", max_length=2, required=False)
    salaryFrom = forms.CharField(label="Зарплата от:", max_length=6,
                                 required=False)
    salaryTo = forms.CharField(label="Зарплата до:", max_length=6, 
                               required=False)
    gender = forms.ChoiceField(label="Пол:", widget=Select, 
                               choices=GENDER_CHOICES)
    searchMode = forms.ChoiceField(label="Режим поиска:", widget=Select,                               choices=SEARCH_MODE_CHOICES, required=True)
    source = forms.MultipleChoiceField(label="Источники:", widget=Select,                                   choices=SOURCE_LIST_CHOICES)
'''

class SearchForm(forms.Form):
    query_text = forms.CharField(label=False, max_length=100, 
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                 "class": "input-xxlarge",
                                 "type": "text"}))
    limit = forms.CharField(label="Число записей с источника:", max_length=30,                        required=False)
    age_from = forms.CharField(label="Возраст от:", max_length=2, 
                              required=False)
    age_to = forms.CharField(label="Возраст до:", max_length=2, required=False)
    salary_from = forms.CharField(label="Зарплата от:", max_length=6,
                                  required=False)
    salary_to = forms.CharField(label="Зарплата до:", max_length=6, 
                                required=False)
    gender = forms.ChoiceField(label="Пол:", widget=Select, 
                               choices=GENDER_CHOICES, required=False)
    mode = forms.ChoiceField(label="Режим поиска:", widget=Select,                               choices=MODE_CHOICES, required=True)
    source = forms.MultipleChoiceField(label="Источники:", widget=Select,                                   choices=SOURCE_CHOICES)
    city = forms.ChoiceField(label="Город:", widget=Select,                         choices=CITY_CHOICES)   

class ParsingForm(forms.Form):
    first_name = forms.CharField(label="Имя:", max_length=40, 
                                 required=True)
    last_name = forms.CharField(label="Фамилия:", max_length=40, 
                                required=True)
    middle_name = forms.CharField(label="Отчество:", max_length=40, 
                                required=True)
    gender = forms.ChoiceField(label="Пол:", widget=Select, choices=                           GENDER_CHOICES, required=False)
    birth = forms.DateField(label="Дата рождения:", required=True,
                            widget=CalendarWidget)
    phone = forms.CharField(label="Телефон:", max_length=11, required=True)
    email = forms.EmailField(label="E-mail:")
    city = forms.ChoiceField(label="Регион:", widget=Select,
                                choices=CITY_CHOICES, required=False)
    degree_of_education = forms.CharField(label="Образование:", 
                                          max_length=40, 
                                          required=True)
    length_of_work = forms.CharField(label="Опыт работы:", max_length=40, 
                                     required=True)
    vacancy = ManyToManyField(label='Вакансия:',
                              required=True)


    def __init__(self, choice_list, selected_list, *args, **kwargs):
        super(ParsingForm, self).__init__(*args, **kwargs)
        self.fields['vacancy'].widget = ManyToManyWidget(choice_list,
                                                         selected_list) 


class SiebelCandidateForm(ModelForm):
    class Meta:
        model = SiebelCandidate
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 
                 'education','email', 'experience', 'gender',
                 'source', 'auto_flag', 'region', 'vacancy',
                 'birth']