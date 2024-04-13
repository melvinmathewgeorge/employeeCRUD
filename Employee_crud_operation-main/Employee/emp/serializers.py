from rest_framework import serializers
from .models import Employee

class EmployeeValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['regid']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'  