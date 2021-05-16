from rest_framework.views import APIView
from rest_framework.response import Response
import random
from .models import *
from .helpers.common import *
from datetime import datetime

def randomDigits(digits):
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)

class ListUsers(APIView):
    def get(self, request, format=None):
        usernames = [user.userID for user in User.objects.all()]
        return json_format(code = 200, message = "Success", data = usernames)

class CreateAccount(APIView):
    
    def post(self, request, format=None):
        users = [user for user in User.objects.all()]
        usernames = [user.username for user in users]
        userids = [user.id for user in users]
        data = request.data
        
        if data["username"] in usernames:
            return json_format(code = 400, message = "Account exist")

        user = User()
        while True:
            id = randomDigits(8)
            if id not in userids:
                user.id = id
                break
        user.username = data["username"]
        user.password = data["password"]
        user.email = data["email"]
        user.phone = data['phone']
        user.sex = data['sex']
        user.address = data["address"]
        user.save()

        if data['role'] == "Manager":
            branch = Branch.objects.get(id=data['branch_id'])
            m = Manager(userid = user, created = datetime.now(), branchid = branch)
            m.save()
        elif data['role'] == "Chiefmanager":
            cm = Chiefmanager(userid = user, cardid = data['card_id'])
            cm.save()
        elif data['role'] == "Accountant":
            branch = Branch.objects.get(id=data['branch_id'])
            a = Accountant(created = datetime.now(), team = data['team'], userid = user, branchid = branch)
            a.save()
        
        return json_format(code = 200, message = "Success")

class SigninViews(APIView):
    
    def post(self, request, format=None):
        users = [user for user in User.objects.all()]
        data = request.data
        for user in users:
            if user.username == data["username"] and user.password == data["password"]:
                return json_format(code = 200, message = "Login successfully")
        
        return json_format(code = 400, message = "Wrong username or password")

class EditInfo(APIView):
    def post(self, request, format = None):
        data = request.data
        user  = User.objects.get(id=data['id'])
        
        user.username = data["username"]
        user.password = data["password"]
        user.email = data["email"]
        user.phone = data['phone']
        user.sex = data['sex']
        user.address = data["address"]
        user.save()

        return json_format(code = 200, message = "Success")

class DeleteAcc(APIView):
    def post(self, request, format = None):
        data = request.data
        user  = User.objects.get(id=data['user_id'])
        print(user.objects.all())

        return json_format(code = 200, message = "Success")

class GetListBranch(APIView):
    def get(self, request, format=None):
        branchs = [{'branch_id': branch.id,
                    'branch_name': branch.name,
                    'branch_location': branch.location} for branch in Branch.objects.all()]
        return json_format(code = 200, message = "Success", data = branchs)

class AddBranch(APIView):
    def post(self, request, format=None):
        branchs = [branch for branch in Branch.objects.all()]
        branch_name = [branch.name for branch in branchs]
        branch_id = [branch.id for branch in branchs]
        data = request.data
        
        if data["branch_name"] in branch_name:
            return json_format(code = 400, message = "Branch exist")

        branch = Branch()
        while True:
            id = randomDigits(8)
            if id not in branch_id:
                branch.id = id
                break
        branch.name = data['branch_name']
        branch.location = data['branch_location']
        branch.save()

        return json_format(code = 200, message = "Success")

class DeleteBranch(APIView):
    def post(self, request, format=None):
        data = request.data
        branch = Branch.objects.get(id=data["branch_id"])
        branch.delete()
        return json_format(code = 200, message = "Success")

class EditInfoBranch(APIView):
    def post(self, request, format = None):
        data = request.data
        branch  = Branch.objects.get(id=data['branch_id'])
        
        branch.name = data["branch_name"]
        branch.location = data["branch_location"]
        branch.save()

        return json_format(code = 200, message = "Success")

class GetDepartment(APIView):
    def get(self, request, format=None):
        departments = [{'department_id': department.id,
                        'branch_id': department.branchid.id,
                        'department_name': department.name,
                        'department_numofemployees': department.numofemployees} for department in Department.objects.all()]

        return json_format(code = 200, message = "Success", data = departments)

class AddDepartment(APIView):
    def post(self, request, format=None):
        departments = [department for department in Department.objects.all()]
        department_name = [department.name for department in departments]
        department_id = [department.id for department in departments]
        data = request.data
        
        if data["department_name"] in department_name:
            return json_format(code = 400, message = "Department exist")

        department = Department()
        while True:
            id = randomDigits(8)
            if id not in department_id:
                department.id = id
                break
        department.name = data['department_name']
        branch = Branch.objects.get(id=data['branch_id'])
        department.branchid = branch
        department.numofemployees = 0
        department.save()

        return json_format(code = 200, message = "Success")

class EditInfoDepartment(APIView):
    def post(self, request, format = None):
        data = request.data
        department  = Department.objects.get(id=data['department_id'])
        
        department.name = data["department_name"]
        branch = Branch.objects.get(id=data['branch_id'])
        department.brandid = branch
        department.save()

        return json_format(code = 200, message = "Success")

class DeleteDepartment(APIView):
    def post(self, request, format=None):
        data = request.data
        department = Department.objects.get(id=data["department_id"])
        department.delete()
        return json_format(code = 200, message = "Success")

class AddEmployee(APIView):
    def post(self, request, format=None):
        employees = [employee for employee in Employee.objects.all()]
        employee_id = [employee.id for employee in employees]
        data = request.data

        employee = Employee()
        while True:
            id = randomDigits(8)
            if id not in employee_id:
                employee.id = id
                break
                
        department = Department.objects.get(id=data['department_id'])
        department.numofemployees += 1
        employee.departmentid = department

        employee.name = data['employee_name']
        employee.phone = data['employee_phone']
        employee.email = data['employee_email']
        employee.address = data['employee_address']
        employee.sex = data['employee_sex']
        employee.exp = data['employee_exp']

        employee.save()
        department.save()

        return json_format(code = 200, message = "Success")


class GetEmployee(APIView):
    def get(self, request, format=None):
        employees = [{'employee_id': employee.id,
                      'department_id': employee.departmentid.id,
                      'employee_name': employee.name,
                      'employee_phone': employee.phone,
                      'employee_email': employee.email,
                      'employee_address': employee.address,
                      'employee_sex': employee.sex,
                      'employee_exp': employee.exp} for employee in Employee.objects.all()]

        return json_format(code = 200, message = "Success", data = employees)

class DeleteEmployee(APIView):
    def post(self, request, format=None):
        data = request.data
        employee = Employee.objects.get(id=data["employee_id"])
        old_department = Department.objects.get(id=employee.departmentid.id)
        old_department.numofemployees -= 1
        old_department.save()
        employee.delete()
        return json_format(code = 200, message = "Success")

class EditInfoEmployee(APIView):
    def post(self, request, format = None):
        data = request.data
        employee  = Employee.objects.get(id=data['employee_id'])
        
        employee.name = data['employee_name']
        employee.phone = data['employee_phone']
        employee.email = data['employee_email']
        employee.address = data['employee_address']
        employee.sex = data['employee_sex']
        employee.exp = data['employee_exp']

        old_department = Department.objects.get(id=employee.departmentid.id)
        old_department.numofemployees -= 1
        old_department.save()

        department = Department.objects.get(id=data['department_id'])
        department.numofemployees += 1
        employee.departmentid = department
        
        department.save()
        employee.save()

        return json_format(code = 200, message = "Success")