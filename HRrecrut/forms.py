from django import forms
from django.utils.translation import ugettext as _
from django.forms.widgets import PasswordInput, RadioSelect, RadioSelect, CheckboxSelectMultiple, Select
from .models import list_of_value


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
    gender = forms.ChoiceField(label="Пол:", widget=RadioSelect, choices=list_of_value().generateSelect('GENDER'), required=False)
    searchMode = forms.ChoiceField(label="Искать:", widget=RadioSelect, choices=list_of_value().generateSelect('SEARCH_MODE'), required=True)
    source = forms.ChoiceField(label="Источник:", widget=CheckboxSelectMultiple, choices=list_of_value().generateSelect('SOURCE_LIST'), required=False)
        
#class SearchOptions(forms.Form):
#    limit = forms.CharField(max_length=30, required=False)
#    itemPage = forms.CharField(max_length=3, required=False)
    
#class AdvancedSearch(forms.Form):
#    ageFrom = forms.CharField(label="Возраст от:", max_length=2, required=False)
#    ageTo = forms.CharField(label="Возраст до:", max_length=2, required=False)
#    salaryFrom = forms.CharField(label='Зарплата от:', max_length=6, required=False)
#    salaryTo = forms.CharField(label='Зарплата до:', max_length=6, required=False)
#    #gender = forms.ChoiceField(label='Пол:', widget=RadioSelect, choices=GENDER_CHOICE)

class PasingForm(forms.Form):
    firstName = forms.CharField(label="Имя:", max_length=40, required=True)
    lastName = forms.CharField(label="Фамилия:", max_length=40, required=True)
    middleName = forms.CharField(label="Отчество:", max_length=40, required=True)
    gender = forms.ChoiceField(label="Пол:", widget=Select, choices=list_of_value().generateSelect('GENDER'), required=False)
    phone = forms.CharField(label="Телефон:", max_length=11, required=True)
    email = forms.EmailField(label="E-mail:")
    location = forms.ChoiceField(label="Регион:", widget=Select, choices=list_of_value().generateSelect('LOCATION'), required=False)
    education = forms.CharField(label="Образование:", max_length=40, required=True)
    experience = forms.CharField(label="Опыт работы:", max_length=40, required=True)
    ##education = forms.ChoiceField(label="Образование:", widget=Select, choices=list_of_value().generateSelect('EDUCATION'), required=False)
    ##expJob = forms.ChoiceField(label="Опыт работы:", widget=Select, choices=list_of_value().generateSelect('YN'), required=False)