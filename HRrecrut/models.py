from django.db import models

# Create your models here.
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
    row_id = models.AutoField(primary_key=True)
    domainName = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    context = models.CharField(max_length=100)
    tagName = models.CharField(max_length=40)
    attributeName = models.CharField(max_length=100)
    attributeValue = models.CharField(max_length=200)
    expression = models.CharField(max_length=100, null=True)
    
    class Meta:
        unique_together  = (("domainName", "context", "target"),)
    
    def generalScheme(self, listDomain=None, context="SEARCH"):
        if(listDomain == None):
            listDomain = SchemaParsing.objects.distinct().values_list('domainName', flat=True)
            
        scheme = {key : {} for key in listDomain}    
        for item in listDomain:
            pasingList = SchemaParsing.objects.filter(domainName=item, context=context).values()
            #print(len(pasingList),pasingList)
            for parStr in pasingList:
                attrVal, target = {}, {}
                attrVal.setdefault(parStr['attributeName'],parStr['attributeValue'])
                target.setdefault('tagName', parStr['tagName'])
                target.setdefault('attrVal', attrVal)
                #print(parStr['expression'])
                target.setdefault('expression', parStr['expression'])
                scheme[parStr['domainName']].setdefault(parStr['target'], target)
        return scheme

        
class SearchObject(models.Model):
    row_id = models.AutoField(primary_key=True)
    domainName = models.CharField(max_length=100)
    SearchMode = models.CharField(max_length=50)
    age = models.BooleanField(default=False)
    gender = models.BooleanField(default=False)
    pay = models.BooleanField(default=False)
    link = models.CharField(max_length=500)
    parametrs = models.CharField(max_length=150) 
 
    class Meta:
        unique_together  = (("domainName", "SearchMode", "age", "gender", "pay", "parametrs", "link"),)
 
    def determinationLink(self, domainName, SearchMode, age=False, gender=False, pay=False):  
        searchObject = SearchObject.objects.filter(domainName=domainName, SearchMode=SearchMode, age=age, gender=gender, pay=pay).values_list('link', flat=True)
        #print('===> ', searchObject)
        return  searchObject[0] 
    def sequenceParametrs(self, domainName, SearchMode, age=False, gender=False, pay=False):  
        sequence = SearchObject.objects.filter(domainName=domainName, SearchMode=SearchMode, age=age, gender=gender, pay=pay).values_list('parametrs', flat=True)
        #print('===> ', sequence)
        return  sequence[0] 


##     
class SearchExtension(models.Model):
    row_id = models.AutoField(primary_key=True)
    par_row = models.OneToOneField(SearchObject, models.CASCADE, primary_key=False, unique=False)
    baseSequence = models.CharField(max_length=100)
    
    class Meta:
        unique_together  = (("par_row", "baseSequence"),)
        

class SearchSequence(models.Model):
    row_id = models.AutoField(primary_key=True)
    #par_row = models.OneToOneField(SearchObject, models.CASCADE, primary_key=False)
    domainName = models.CharField(max_length=100,unique=True)
    baseSequence = models.CharField(max_length=100)
    
    class Meta:
        unique_together  = ("baseSequence","domainName")##,) ##(("par_row", "baseSequence"),) "domainName", "domainName",
        
    def getBaseSequence(self, domainName):
        sequence = SearchSequence.objects.filter(domainName=domainName).values_list('baseSequence', flat=True)
        return sequence[0]        
 
        
        
class VailidValues(models.Model):
    row_id = models.AutoField(primary_key=True)
    domainName = models.CharField(max_length=100) ## FK
    criterionName = models.CharField(max_length=50)
    rawValue = models.CharField(max_length=50, null=True)
    validValue = models.CharField(max_length=50, null=True)
    expression = models.CharField(max_length=100, null=True)
    
    class Meta:
        unique_together  = (("domainName", "criterionName", "rawValue", "validValue", "expression"),)
    
    def generateValidDict(self, domainName, criterionName):
        validValue = {}
        listVal = VailidValues.objects.filter(domainName=domainName, criterionName=criterionName).values('rawValue','validValue','expression')
        if(len(listVal) == 0):
            return None
            
        for item in listVal:
            #print(item)
            if(item['rawValue'] != None and item['validValue'] != None and item['expression'] == None):
                validValue.setdefault(item['rawValue'], item['validValue'])
            elif(item['rawValue'] != None and item['validValue'] == None and item['expression'] != None):
                validValue.setdefault(item['rawValue'], eval(item['expression']))
            elif(item['rawValue'] == None and item['validValue'] == None and item['expression'] != None):
                validValue = eval(item['expression'])
            else:
                continue
        
        return validValue
    
#class OtherAuth(models.Model):
#    row_id = models.AutoField(primary_key=True)
#    domainName = models.CharField(max_length=100)
#    otherUserName = models.CharField(max_length=100)
#    otherPass = models.CharField(max_length=100)
#    client_id = models.CharField(max_length=100)
#    authoCode = models.CharField(max_length=100, null=True)
#    auth_cookis =  models.CharField(max_length=100, null=True)
#    access_token = models.CharField(max_length=100, null=True)
#    refresh_token = models.CharField(max_length=100, null=True)
#    link =  models.CharField(max_length=500)
#    ##user = models.ForeignKey(User)
#    
#    class Meta:
#        nique_together  = (("domainName", "otherUserName", "otherPass", "link"),)
#        
#        
#    def getAuthParamers(self, domainName):
#        return self.objects.filter(domainName=domainName).values('otherUserName','otherPass','client_id','authoCode', 'link')[0]
#        
#    def getAuth(self, domainName):
#        return self.objects.filter(domainName=domainName).values('auth_cookis','access_token','refresh_token')[0]
#        