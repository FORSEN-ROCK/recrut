from django.contrib import admin
from django.forms.widgets import MultipleHiddenInput
from .models import *


# Custom class "ModelAdmin" for siebel
class SiebelBDModelAdmin(admin.ModelAdmin):
    using = 'siebel'

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super(SiebelBDModelAdmin, 
                     self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None,
                                 **kwargs):
        return super(SiebelBDModelAdmin, 
                     self).formfield_for_foreignkey(
                                      db_field, request=request,
                                      using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request=None,
                                 **kwargs):
        return super(SiebelBDModelAdmin,
                     self).formfield_for_manytomany(
                                    db_field, request=request, 
                                    using=self.using, **kwargs
        ) 


class SiebelStackedInline(admin.TabularInline):
    using = 'siebel'
    extra = 0
    

    def get_queryset(self, request):
        return super(SiebelStackedInline, 
                     self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None,
                                 **kwargs):
        return super(SiebelStackedInline, 
                     self).formfield_for_foreignkey(
                                      db_field, request=request,
                                      using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request=None,
                                 **kwargs):
        return super(SiebelStackedInline,
                     self).formfield_for_manytomany(
                                    db_field, request=request, 
                                    using=self.using, **kwargs
        )


# Models for admin view
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name','descriptions', 'login_link', 'test_link',
                    'inactive')
    search_fields = ('domainName',)


class SearchPatternAdmin(admin.ModelAdmin):    
    list_display = ('query_text', 'age_from', 'age_to', 'salary_from',
                    'salary_to', 'gender', 'city', 'source', 'mode',
                    'user')


class SearchKeyAdmin(admin.ModelAdmin):
    list_display = ('text', 'created', 'repeat', 'first_load', 'reload',
                    'count_load')


class LoadResumeLogAdmin(admin.ModelAdmin):
    list_display = ('title_resume', 'last_update', 'url')


class KeyWordsAdmin(admin.ModelAdmin):
    list_display = ('resume', 'key_text', 'source')


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('resume', 'experience_period', 'last_position',
                    'organization_name', 'experience_text', 'source')


class EducationAdmin(admin.ModelAdmin):
    list_display = ('resume', 'year', 'name', 'profession', 'source')


class SearchResultAdmin(admin.ModelAdmin):
    list_display = ('title_resume', 'gender', 'age', 'salary',
                    'length_of_work', 'degree_of_education',
                    'city', 'last_update', 'source',
                    'search_text', 'preview')

class RequestHeadersAdmin(admin.ModelAdmin):
    list_display = ('sectionName', 'body', 'credentials')


################################Siebel##################################
class SiebelCandidateAdmin(SiebelBDModelAdmin):
    list_display = ('created', 'created_by', 'last_upd_by', 
                    'first_name', 'last_name',
                    'middle_name', 'education', 'email', 'phone',
                    'experience', 'gender', 'source', 'auto_flag',
                    'region')#'resume_text',)


class SiebelVacancyAdmin(SiebelBDModelAdmin):
    list_display = ('created', 'created_by', 'last_upd', 'last_upd_by',
                    'status_date', 'job_name', 'status')


class SiebelCommunicationAddresAdmin(SiebelBDModelAdmin):
    list_display = ('created', 'created_by', 'last_upd', 'last_upd_by',
                    'addr', 'comm_medium', 'candidate')


# Register your models here.

admin.site.register(Domain, DomainAdmin)
#admin.site.register(Credentials)
#admin.site.register(CredentialsData)
#admin.site.register(RequestHeaders, RequestHeadersAdmin)
#admin.site.register(SessionData)
#admin.site.register(SearchPattern, SearchPatternAdmin)
admin.site.register(SearchKey, SearchKeyAdmin)
admin.site.register(LoadResumeLog, LoadResumeLogAdmin)
admin.site.register(KeyWords, KeyWordsAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(SearchResult, SearchResultAdmin)

################################Siebel##################################
admin.site.register(SiebelCandidate, SiebelCandidateAdmin)
admin.site.register(SiebelVacancy, SiebelVacancyAdmin)
admin.site.register(SiebelCommunicationAddres,
                    SiebelCommunicationAddresAdmin)