from django.contrib import admin
from polls.models import Poll
from polls.models import Choice

class ChoiceInline(admin.TabularInline):
    model=Choice
    extra=3
    
class PollAdmin(admin.ModelAdmin):
   
    fieldsets=[
        ('hello'          ,{'fields':['question']}),
        ('Date infomation',{'fields':['pub_date'],'classes':['collapse']}),
    ]
    #fields=['pub_date','question']
    inlines=[ChoiceInline]
    list_display=('question','pub_date','was_published_recently','hello')
    list_filter=['pub_date']
admin.site.register(Poll,PollAdmin)

