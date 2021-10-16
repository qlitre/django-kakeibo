from django.contrib import admin
from .models import Payment, Income, PaymentCategory, IncomeCategory
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment


class PaymentAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    list_display = ['date', 'category', 'price', 'description']
    list_filter = ('category',)
    ordering = ('-date',)

    resource_class = PaymentResource


class PaymentCategoryResource(resources.ModelResource):
    class Meta:
        model = PaymentCategory


class PaymentCategoryAdmin(ImportExportModelAdmin):
    resource_class = PaymentCategoryResource


class IncomeResource(resources.ModelResource):
    class Meta:
        model = Income


class IncomeAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    list_display = ['date', 'category', 'price', 'description']
    list_filter = ('category',)
    ordering = ('-date',)

    resource_class = IncomeResource


class IncomeCategoryResource(resources.ModelResource):
    class Meta:
        model = IncomeCategory


class IncomeCategoryAdmin(ImportExportModelAdmin):
    resource_class = IncomeCategoryResource


admin.site.register(PaymentCategory, PaymentCategoryAdmin)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Income, IncomeAdmin)
