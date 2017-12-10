from django.contrib import admin
from .models import *
# Models for admin view

class list_of_valueAdmin(admin.ModelAdmin):
    list_display = ('type','lang_id','name','value')

class SearchObjectAdmin(admin.ModelAdmin):
    list_display = ('domain','SearchMode','age','gender','pay','link','parametrs','iterator','iterStep','startPosition')
    search_fields = ('SearchMode',)

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('firstName','lastName','middleName','gender','phone','email','location','education','experience')
    search_fields = ('firstName','lastName','middleName','phone','email')

class ResumeLinkAdmin(admin.ModelAdmin):
    list_display = ('url','resume')
    search_fields = ('resume',)
    
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domainName','descriptions','rootUrl','preview','itemRecord')
    search_fields = ('domainName',)
    
class VailidValuesAdmin(admin.ModelAdmin):
    list_display = ('criterionName','rawValue','validValue','context','domain')
    search_fields = ('criterionName','context')
    
class ExpressionAdmin(admin.ModelAdmin):
    list_display = ('SchemaParsing','split','shearTo','shearFrom','sequence','regexp','seqOper','join')

class SearchCardAdmin(admin.ModelAdmin):
    list_display = ('text','ageFrom','ageTo','salaryFrom','salaryTo','gender')
    
class TableColumnHeadAdmin(admin.ModelAdmin):
    list_display = ('displayName','fieldName','tableName')
# Register your models here.

admin.site.register(list_of_value, list_of_valueAdmin)
admin.site.register(SchemaParsing)
admin.site.register(SearchObject, SearchObjectAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Expression, ExpressionAdmin)
admin.site.register(VailidValues, VailidValuesAdmin)
admin.site.register(Credentials)
admin.site.register(CredentialsData)
admin.site.register(RequestHeaders)
admin.site.register(SessionData)
admin.site.register(SearchCard, SearchCardAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(ResumeLink, ResumeLinkAdmin)
admin.site.register(TableColumnHead, TableColumnHeadAdmin)