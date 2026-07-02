from django.contrib import admin
from .models import TheoryExamination, PracticalExamination

@admin.register(TheoryExamination)
class TheoryExaminationAdmin(admin.ModelAdmin):
    readonly_fields = ('amount_per_script', 'valuation_charge', 'total', 'income_tax_10percent', 'amount_after_tds',  'net_payable')

    list_display = ('name', 'subject_code', 'valuation_charge', 'income_tax_10percent', 'amount_after_tds', 'total', 'net_payable')
@admin.register(PracticalExamination)
class PracticalExaminationAdmin(admin.ModelAdmin):
    readonly_fields = ('remuneration_before_tds', 'tds_10percent', 'remuneration_after_tds', 'total_remuneration', 'total')
    list_display = ('name_and_address', 'course_code', 'remuneration_before_tds', 'tds_10percent', 'remuneration_after_tds', 'total_remuneration', 'total')
