from django import forms
from .models import TheoryExamination, PracticalExamination

class TheoryExaminationFormStep1(forms.ModelForm):
    class Meta:
        model = TheoryExamination
        fields = ['evaluator_type', 'dept', 'sem', 'name', 'college', 'subject_code', 'no_of_scripts']

class TheoryExaminationFormStep2(forms.ModelForm):
    class Meta:
        model = TheoryExamination
        fields = ['reviewer_charge', 'da', 'ta', 'pan', 'ifsc_code', 'bank_account_number']

class PracticalExaminationStep1Form(forms.ModelForm):
    class Meta:
        model = PracticalExamination
        fields = ['name_and_address', 'course_code', 'no_of_days', 'batch_no', 'no_of_students', 'amount_of_batch']

class PracticalExaminationStep2Form(forms.ModelForm):
    class Meta:
        model = PracticalExamination
        fields = ['ta', 'da', 'pan', 'ifsc_code', 'account_number']
