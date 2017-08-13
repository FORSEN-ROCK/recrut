from django.contrib import admin
from .models import list_of_value, SearchObject, SchemaParsing
# Register your models here.


admin.site.register(list_of_value)
admin.site.register(SchemaParsing)
admin.site.register(SearchObject)