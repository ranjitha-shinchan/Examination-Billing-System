from django.db import models
from decimal import Decimal

class TheoryExamination(models.Model):
    VALUATOR_TYPE_CHOICES = [
        ('Valuator', 'Valuator'),
        ('Reviewer', 'Reviewer'),
    ]
    
    evaluator_type = models.CharField(choices=VALUATOR_TYPE_CHOICES, max_length=10)
    dept = models.CharField(max_length=100)
    sem = models.IntegerField()  # removed max_length because IntegerField doesn't accept it
    name = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=100)
    no_of_scripts = models.IntegerField()
    amount_per_script = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('30.00'))
    
    # Calculated Fields
    valuation_charge = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    reviewer_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    income_tax_10percent = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    amount_after_tds = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    da = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  
    ta = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  
    net_payable = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    pan = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=20)
    bank_account_number = models.CharField(max_length=20)

    def calculate_valuation_charge(self):
        return Decimal(self.no_of_scripts) * Decimal(self.amount_per_script)

    def calculate_income_tax(self):
        return ((self.valuation_charge + self.reviewer_charge) * Decimal('10')) / Decimal('100')

    def calculate_amount_after_tax(self):
        return (self.valuation_charge + self.reviewer_charge) - self.income_tax_10percent

    def calculate_net_payable(self):
        return self.amount_after_tds + Decimal(self.da) + Decimal(self.ta)

    def calculate_total(self):
        return self.valuation_charge + self.reviewer_charge  

    def save(self, *args, **kwargs):
        self.valuation_charge = self.calculate_valuation_charge()
        self.income_tax_10percent = self.calculate_income_tax()
        self.amount_after_tds = self.calculate_amount_after_tax()
        self.net_payable = self.calculate_net_payable()
        self.total = self.calculate_total()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.subject_code} - {self.college}"


class PracticalExamination(models.Model):
    name_and_address = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    no_of_days = models.IntegerField()
    batch_no = models.IntegerField()
    no_of_students = models.IntegerField()
    amount_of_batch = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Calculated Fields
    remuneration_before_tds = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    tds_10percent = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    remuneration_after_tds = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    ta = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  
    da = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  
    total_remuneration = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))
    pan = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=20)
    account_number = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=Decimal('0.00'))

    def calculate_remuneration_before_tds(self):
        # Assuming remuneration = no_of_days * amount_of_batch
        return Decimal(self.no_of_days) * self.amount_of_batch

    def calculate_tds_10percent(self):
        return (self.remuneration_before_tds * Decimal('10')) / Decimal('100')

    def calculate_remuneration_after_tds(self):
        return self.remuneration_before_tds - self.tds_10percent

    def calculate_total_remuneration(self):
        return self.remuneration_after_tds + Decimal(self.ta) + Decimal(self.da)

    def calculate_total(self):
        return self.total_remuneration

    def save(self, *args, **kwargs):
        self.remuneration_before_tds = self.calculate_remuneration_before_tds()
        self.tds_10percent = self.calculate_tds_10percent()
        self.remuneration_after_tds = self.calculate_remuneration_after_tds()
        self.total_remuneration = self.calculate_total_remuneration()
        self.total = self.calculate_total()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name_and_address} - {self.course_code} - {self.total_remuneration}"
