from django.contrib import admin
# Register your models here.
from api.models import User,Profile, Plant
 

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'email']


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['id','user', 'full_name' ,'verified']

admin.site.register(User, UserAdmin)
admin.site.register( Profile,ProfileAdmin)
admin.site.register(Plant)
