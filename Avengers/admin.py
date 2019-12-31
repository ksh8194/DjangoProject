from django.contrib import admin
from Avengers.models import Myinfo,Schedule
import Avengers

# Register your models here.
class MyinfoAdmin(admin.ModelAdmin):
    list_display = ('id','email','pwd')
    
admin.site.register(Myinfo,MyinfoAdmin)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('no','memid','title','content','date','star')
    

admin.site.register(Schedule,ScheduleAdmin)