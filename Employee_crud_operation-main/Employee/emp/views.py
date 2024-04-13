from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Employee
from .serializers import  EmployeeSerializer


class EmployeeAPIView(APIView):
    # Handle POST request to create a new employee
    def post(self, request):
        try:
            serializer = EmployeeSerializer(data=request.data)
            if serializer.is_valid():
                # Check if email already exists
                if self.checkDuplicateEmail(serializer.validated_data['email']):
                    return Response({"message": "Employee already exists", "success": False}, status=status.HTTP_200_OK)
                serializer.save()
                return Response({"message": "Employee created successfully", "regid": serializer.data['regid'], "success": True}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid request body",  "success": False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Employee creation failed", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Handle PUT request to update an existing employee
    def put(self, request):
        try:
            regId = request.data.get('regid')
            employee = Employee.objects.get(regid=regId)
            serializer = EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Employee details updated successfully", "success": True}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid request body",  "success": False}, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"message": "No employee found with this regId", "success": False}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Employee update failed", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Handle DELETE request to delete an existing employee
    def delete(self, request):
        try:
            regId = request.data.get('regid')
            employee = Employee.objects.get(regid=regId)
        except Employee.DoesNotExist:
            return Response({"message": "No employee found with this regId", "success": False}, status=status.HTTP_200_OK)

        employee.delete()
        return Response({"message": "Employee deleted successfully", "success": True}, status=status.HTTP_200_OK)

    # Handle GET request to retrieve details of an employee
    def get(self, request):
        regId = request.query_params.get('regid')
        if regId:
            try:
                employee = Employee.objects.get(regid=regId)
                serializer = EmployeeSerializer(employee)
                return Response({"message": "Employee details found", "success": True, "employees": [serializer.data]}, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                return Response({"message": "Employee details not found", "success": False,"employees": []}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Please provide an Employee ID", "success": True, "employees": []}, status=status.HTTP_200_OK)

    # Check if email already exists
    def checkDuplicateEmail(self, email):
        try:
            employee = Employee.objects.get(email=email)
            return True
        except Employee.DoesNotExist:
            return False