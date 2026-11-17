from django.contrib import admin
from .models import BankProfile,Vacancy,Application
@admin.register(BankProfile)
class BankProfileAdmin(admin.ModelAdmin):
    list_display=('name','short_name','active','created_at'); list_filter=('active',); search_fields=('name','short_name')
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display=('title','bank','department','openings','closing_date','active'); list_filter=('bank','active','department'); search_fields=('title','bank__name')
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display=('reference','full_name','vacancy','submitted_at'); list_filter=('vacancy__bank','vacancy'); search_fields=('reference','full_name','email'); readonly_fields=('reference','submitted_at')
    def has_add_permission(self,request): return False
