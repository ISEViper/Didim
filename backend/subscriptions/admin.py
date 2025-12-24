from django.contrib import admin
from .models import Plan, Subscription, Payment

# Register your models here.
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)

admin.site.register(Subscription)
admin.site.register(Payment)