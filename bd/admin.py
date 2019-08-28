# -*-coding: UTF-8-*- #

from django.contrib import admin
from .models import Charge,Song,Praise,Instrument,Designation,Cell,Member,Ministry,Institution,MoneyTransaction,member_praises, Ministry_Directing

#-----------InLine----------
# class directingChurchInline(admin.StackedInline):
#     model = Church_Member
#     extra = 1

class MemberPraisesInLine(admin.StackedInline):
    model = member_praises
    extra = 1

class MinistryInLine(admin.StackedInline):
    model = Ministry_Directing
    extra = 1

class SongsInLine(admin.TabularInline):
    model = Praise.Songs.through

#-----------InLine----------

#-----------Admin----------
class CellAdmin(admin.ModelAdmin):
    list_display = ['address','directing','host']

class ChargeAdmin(admin.ModelAdmin):
    list_display = ['name','maxCount','get_members']

class MemberAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('dni','name','gender','address','phone','level','occupation','get_praises')
    #inlines = [directingChurchInline]

    # def make_name(self, queryset):
    #     queryset.update(name = 'amelia')
    # make_name.short_description = 'Test'

class SongAdmin(admin.ModelAdmin):
    list_display = ('name','author','status')
    actions = ['change_to_approved','change_to_denied','change_to_pending']
    list_filter = ['status']
    inlines = [SongsInLine]

    def change_to_approved(selfself,request,queryset):
        queryset.update(status = 'approved')

    def change_to_denied(selfself,request,queryset):
        queryset.update(status = 'denied')

    def change_to_pending(selfself,request,queryset):
        queryset.update(status = 'pending')

class PraiseAdmin(admin.ModelAdmin):
    list_display = ['date','get_songs']
    inlines = [MemberPraisesInLine]
    list_filter = ['date']
    #exclude = ['Songs']

# class ChurchAdmin(admin.ModelAdmin):
#     list_display = ('name','address','phone','designation')

class MoneyTransactionAdmin(admin.ModelAdmin):
    list_display = ('date','amount','description','status','institution','member')
    exclude = ['status']
    list_filter = ['date','status','type']
    actions = ['make_confirm']
    #list_editable = ['status']

    def make_confirm(self, queryset):
        queryset.update(status='True')
    make_confirm.short_description = 'Cambiar estado'

class MinistryAdmin(admin.ModelAdmin):
    inlines = [MinistryInLine]
    list_display = ['name','get_directings','get_members']
#-----------Admin----------

#----------Other----------
admin.site.register(Cell,CellAdmin)
# admin.site.register(Church,ChurchAdmin)
admin.site.register(Designation)
admin.site.register(Institution)
admin.site.register(Instrument)
admin.site.register(Member,MemberAdmin)
admin.site.register(Ministry,MinistryAdmin)
admin.site.register(MoneyTransaction,MoneyTransactionAdmin)
admin.site.register(Praise,PraiseAdmin)
admin.site.register(Song,SongAdmin)
admin.site.register(Charge,ChargeAdmin)