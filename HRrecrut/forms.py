from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from django.forms.widgets import PasswordInput, RadioSelect, CheckboxSelectMultiple, Select, SelectMultiple, MultiWidget
from .models import list_of_value, Resume, SearchCard

#Custom field

#Choices List

GENDER_CHOICES = [(item.name,item.value) for item in list_of_value.objects.filter(type='GENDER')]
LOCATION_CHOICES = [(item.name,item.value) for item in list_of_value.objects.filter(type='LOCATION')]
SEARCH_MODE_CHOICES = [(item.name,item.value) for item in list_of_value.objects.filter(type='SEARCH_MODE')]
SOURCE_LIST_CHOICES = [(item.name,item.value) for item in list_of_value.objects.filter(type='SOURCE_LIST')]


class ResumeRecord(forms.Form):
    firstName = forms.CharField(label="Имя" ,max_length=50)
    lastName = forms.CharField(label="Фамилия" ,max_length=50)
    middleName = forms.CharField(label="Отчество" ,max_length=50)
    gender = forms.ChoiceField(label="Пол" ,widget=Select, choices=GENDER_CHOICES)
    phone = forms.CharField(label="Телефон" ,max_length=12)
    email = forms.EmailField(label="E-mail" ,required=True)
    location = forms.CharField(label="Регион" ,max_length=100)
    education = forms.CharField(label="Образование" ,max_length=100)
    experience = forms.CharField(label="Опыт работы" ,max_length=50)


class AuthorizationForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", max_length=60, required=True)
    password = forms.CharField(label="Пароль", max_length=32, widget=PasswordInput, required=True)

class SearchForm(forms.Form):
    text = forms.CharField(label=False, max_length=100, required=True)
    limit = forms.CharField(label="Число записей с источника:", max_length=30, required=False)
    itemPage = forms.CharField(label="Число записей на странице:", max_length=3, required=False)
    ageFrom = forms.CharField(label="Возраст от:", max_length=2, required=False)
    ageTo = forms.CharField(label="Возраст до:", max_length=2, required=False)
    salaryFrom = forms.CharField(label="Зарплата от:", max_length=6, required=False)
    salaryTo = forms.CharField(label="Зарплата до:", max_length=6, required=False)
    gender = forms.ChoiceField(label="Пол:", widget=Select, choices=GENDER_CHOICES)#RadioSelect
    searchMode = forms.ChoiceField(label="Режим поиска:", widget=Select, choices=SEARCH_MODE_CHOICES, required=True)
    source = forms.MultipleChoiceField(label="Источники:", widget=Select, choices=SOURCE_LIST_CHOICES)
        

class PasingForm(forms.Form):
    firstName = forms.CharField(label="Имя:", max_length=40, required=True)
    lastName = forms.CharField(label="Фамилия:", max_length=40, required=True)
    middleName = forms.CharField(label="Отчество:", max_length=40, required=True)
    gender = forms.ChoiceField(label="Пол:", widget=Select, choices=GENDER_CHOICES, required=False)
    phone = forms.CharField(label="Телефон:", max_length=11, required=True)
    email = forms.EmailField(label="E-mail:")
    location = forms.ChoiceField(label="Регион:", widget=Select, choices=LOCATION_CHOICES, required=False)
    education = forms.CharField(label="Образование:", max_length=40, required=True)
    experience = forms.CharField(label="Опыт работы:", max_length=40, required=True)

class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['firstName','lastName','middleName','gender','phone','email','location','education','experience']

class SearchCardForm(ModelForm):
    class Meta:
        model = SearchCard
        fields = ['text','ageFrom','ageTo','salaryFrom','salaryTo','gender']