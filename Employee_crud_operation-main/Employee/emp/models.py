from django.db import models
from . import mixins

class Employee(mixins.GenericModelMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=15,null=True)  
    address_details = models.JSONField(null=True, blank=True)  
    work_experience = models.JSONField(null=True, blank=True) 
    qualifications = models.JSONField(null=True, blank=True) 
    projects = models.JSONField(null=True, blank=True) 
    photo = models.TextField(null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.regid:
            last_emp = Employee.objects.order_by('-regid').first()
            if last_emp:
                last_emp_number = int(last_emp.regid[3:])  # Extract the numeric part
                self.regid = 'EMP{:03d}'.format(last_emp_number + 1)
            else:
                self.regid = 'EMP001'
        super().save(*args, **kwargs)