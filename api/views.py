from rest_framework.views import APIView
from rest_framework.response import Response
import random
from .models import *
from .helpers.common import *
import datetime
from calendar import monthrange

def randomDigits(digits, index):
    lower = 10**(digits-1)
    return lower + index

class ListUsers(APIView):
    def get(self, request, format=None):
        data = request.data
        users = [user for user in User.objects.all()]
        return_data = []
        if "id" in data.keys():
            userid = data['id']
        else:
            userid = None
        for user in users:
            tmp = {}
            tmp["user_id"] = user.id
            tmp["username"] = user.username
            tmp["password"] = user.password
            tmp["email"] = user.email
            tmp["address"] = user.address
            tmp["sex"] = user.sex
            if userid == user.id:
                return_data = tmp
                break
            return_data.append(tmp)

        return json_format(code = 200, message = "Success", data = return_data)

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
            id = randomDigits(8, len(users))
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
            m = Manager(userid = user, created = datetime.datetime.now(), branchid = branch)
            m.save()
        elif data['role'] == "Chiefmanager":
            cm = Chiefmanager(userid = user)
            cm.save()
        elif data['role'] == "Accountant":
            branch = Branch.objects.get(id=data['branch_id'])
            a = Accountant(created = datetime.datetime.now(), userid = user, branchid = branch)
            a.save()
        
        return json_format(code = 200, message = "Success")

class SigninViews(APIView):
    
    def post(self, request, format=None):
        users = [user for user in User.objects.all()]
        type_acc = np.array(["Manager", "Chiefmanager", "Accountant"])
        data = request.data
        for user in users:
            
            if user.username == data["username"] and user.password == data["password"]:
                list1 = np.array([Manager.objects.filter(userid=user.id).count(), Chiefmanager.objects.filter(userid=user.id).count(), \
                    Accountant.objects.filter(userid=user.id).count()])
                data = {"id": user.id,
                        "account_type" : type_acc[list1 != 0][0]}
                return json_format(code = 200, message = "Login successfully", data = data)
        
        return json_format(code = 400, message = "Wrong username or password")

class EditInfo(APIView):
    def post(self, request, format = None):
        data = request.data
        user  = User.objects.get(id=data['id'])
        
        user.username = data["username"]
        # user.password = data["password"]
        user.email = data["email"]
        user.phone = data['phone']
        user.sex = data['sex']
        user.address = data["address"]
        user.save()

        return json_format(code = 200, message = "Success")

class DeleteAcc(APIView):
    def post(self, request, format = None):
        data = request.data
        id = data['user_id']
        user = User.objects.get(id=id)
        user.delete()
        return json_format(code = 200, message = "Success")

class GetListBranch(APIView):
    def get(self, request, format=None):
        data = request.data
        if "branch_id" not in data.keys():
            branchs = [{'branch_id': branch.id,
                        'branch_phone': branch.phone,
                        'branch_location': branch.location} for branch in Branch.objects.all()]
        else:
            branch =  Branch.objects.get(id=data['id'])
            branchs = {'branch_id': branch.id,
                        'branch_phone': branch.phone,
                        'branch_location': branch.location}
        return json_format(code = 200, message = "Success", data = branchs)

class AddBranch(APIView):
    def post(self, request, format=None):
        branchs = [branch for branch in Branch.objects.all()]
        branch_phone = [branch.phone for branch in branchs]
        branch_id = [branch.id for branch in branchs]
        data = request.data
        
        if data["branch_phone"] in branch_phone:
            return json_format(code = 400, message = "Branch exist")

        branch = Branch()
        while True:
            id = randomDigits(8, len(branch_id))
            if id not in branch_id:
                branch.id = id
                break
        branch.phone = data['branch_phone']
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
        
        if "branch_phone" in data.keys():
            branch.phone = data["branch_phone"]
        if "branch_location" in data.keys():
            branch.location = data["branch_location"]
        branch.save()

        return json_format(code = 200, message = "Success")

class GetDepartment(APIView):
    def get(self, request, format=None):
        data = request.data
        if "department_id" in data.keys():
            department = Department.objects.get(id=data['department_id'])
            departments = {'department_id': department.id,
                        'branch_id': department.branchid.id,
                        'department_name': department.name,
                        'department_numofemployees': department.numofemployees} 
        else:
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
            id = randomDigits(8, len(departments))
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
        
        if "department_name" in data.keys():
            department.name = data["department_name"]
        if "branch_id" in data.keys():
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

class AddTax(APIView):
    def post(self, request, format=None):
        taxes_id = [tax.taxtype for tax in Tax.objects.all()]
        data = request.data

        tax = Tax()
        while True:
            id = randomDigits(8, len(taxes_id))
            if id not in taxes_id:
                tax.id = id
                break
        tax.taxtype = data['taxtype']
        tax.percentage = data['percentage']
        tax.save()

        return json_format(code = 200, message = "Success")

class AddEmployee(APIView):
    def post(self, request, format=None):
        employees = [employee for employee in Employee.objects.all()]
        employee_id = [employee.id for employee in employees]
        data = request.data

        employee = Employee()
        while True:
            id = randomDigits(8, len(employee_id))
            if id not in employee_id:
                employee.id = id
                break
                
        department = Department.objects.get(id=data['department_id'])
        department.numofemployees += 1
        employee.departmentid = department

        tax = Tax.objects.get(id=data['taxid'])
        employee.taxid = tax
        employee.name = data['employee_name']
        employee.phone = data['employee_phone']
        employee.email = data['employee_email']
        employee.address = data['employee_address']
        employee.sex = data['employee_sex']
        employee.exp = data['employee_exp']
        employee.salarydefault = data['employee_salary']
        employee.coef = data['employee_coef']

        employee.save()
        department.save()

        return json_format(code = 200, message = "Success")


class GetEmployee(APIView):
    def get(self, request, format=None):
        data = request.data
        if "employee_id" in data.keys():
            employee = Employee.objects.get(id=data['employee_id'])
            employees = {'employee_id': employee.id,
                        'department_id': employee.departmentid.id,
                        'employee_name': employee.name,
                        'employee_taxid': employee.taxid.id,
                        'employee_phone': employee.phone,
                        'employee_email': employee.email,
                        'employee_address': employee.address,
                        'employee_sex': employee.sex,
                        'employee_exp': employee.exp,
                        'employee_salary': employee.salarydefault,
                        'employee_coef': employee.coef} 
        else:
            employees = [{'employee_id': employee.id,
                        'department_id': employee.departmentid.id,
                        'employee_name': employee.name,
                        'employee_taxid': employee.taxid.id,
                        'employee_phone': employee.phone,
                        'employee_email': employee.email,
                        'employee_address': employee.address,
                        'employee_sex': employee.sex,
                        'employee_exp': employee.exp,
                        'employee_salary': employee.salarydefault,
                        'employee_coef': employee.coef} for employee in Employee.objects.all()]

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
        tax = Tax.objects.get(id=data['taxid'])
        employee.taxid = tax
        employee.name = data['employee_name']
        employee.phone = data['employee_phone']
        employee.email = data['employee_email']
        employee.address = data['employee_address']
        employee.sex = data['employee_sex']
        employee.exp = data['employee_exp']
        employee.salarydefault = data['employee_salary']
        employee.coef = data['employee_coef']

        old_department = Department.objects.get(id=employee.departmentid.id)
        old_department.numofemployees -= 1
        old_department.save()

        department = Department.objects.get(id=data['department_id'])
        department.numofemployees += 1
        employee.departmentid = department
        
        department.save()
        employee.save()

        return json_format(code = 200, message = "Success")

class AddSalary(APIView):
    def post(self, request, format=None):
        data = request.data
        salaries_id = [salary.id for salary in Salary.objects.all()]

        salary = Salary()
        while True:
            id = randomDigits(8, len(salaries_id))
            if id not in salaries_id:
                salary.id = id
                break
        
        salary.fine = data['fine']
        salary.reward = data['reward']

        employee = Employee.objects.get(id=data['employee_id'])
        salary.employeeid = employee

        m, y = [int(i) for i in data['salary_table'].split("/")]
        days = ['{:04d}-{:02d}-{:02d}'.format(y, m, d) for d in range(1, monthrange(y, m)[1] + 1)]
        start_date = datetime.date(*(int(s) for s in days[0].split('-')))
        end_date = datetime.date(*(int(s) for s in days[-1].split('-')))
        total = employee.salarydefault * employee.coef - salary.fine + salary.reward
        salary_tables = [salary_table for salary_table in Salarytable.objects.all()]
        salary_tables_id = [salary_table.id for salary_table in salary_tables]
        exist_salary_table = False
        for salary_table in salary_tables:
            if (start_date == salary_table.startdate) and (end_date == salary_table.enddate):
                exist_salary_table = True
                salary_table.total += total
                salary_table.save()
                salary.salarytableid = salary_table
                break

        if not exist_salary_table:
            salaryTable = Salarytable()
            while True:
                id = randomDigits(8, len(salary_tables))
                if id not in salary_tables_id:
                    salaryTable.id = id
                    break
            salaryTable.note = ""
            salaryTable.startdate = start_date
            salaryTable.enddate = end_date
            salaryTable.total = total
            salaryTable.save()

            salary.salarytableid = salaryTable
        
        salary.save()

        return json_format(code = 200, message = "Success")

class GetSalaryByEmployee(APIView):
    def get(self, request, format=None):
        data = request.data
        salaries = [{'salary_id': salary.id,
                   'employeeid': salary.employeeid.id,
                   'salarytableid': salary.salarytableid.id,
                   'fine': salary.fine,
                   'reward': salary.reward} for salary in Salary.objects.filter(employeeid__id=data['employeeid'])]

        return json_format(code = 200, message = "Success", data = salaries)

class GetSalary(APIView):
    def get(self, request, format=None):
        data = request.data
        if 'salary_id' in data.keys():
            salary = Salary.objects.get(id=data['salary_id'])
            salaries = {'salary_id': salary.id,
                    'employeeid': salary.employeeid.id,
                    'salarytableid': salary.salarytableid.id,
                    'fine': salary.fine,
                    'reward': salary.reward}

        else:
            salaries = [{'salary_id': salary.id,
                   'employeeid': salary.employeeid.id,
                   'salarytableid': salary.salarytableid.id,
                   'fine': salary.fine,
                   'reward': salary.reward} for salary in Salary.objects.all()]

        return json_format(code = 200, message = "Success", data = salaries)

class GetSalaryTable(APIView):
    def get(self, request, format=None):
        data = request.data

        m, y = [int(i) for i in data['salary_table'].split("/")]
        days = ['{:04d}-{:02d}-{:02d}'.format(y, m, d) for d in range(1, monthrange(y, m)[1] + 1)]
        start_date = datetime.date(*(int(s) for s in days[0].split('-')))
        end_date = datetime.date(*(int(s) for s in days[-1].split('-')))
        
        
        salary_tables = [salary_table for salary_table in Salarytable.objects.all()]
        salary_table_id = None
        for salary_table in salary_tables:
            if (start_date == salary_table.startdate) and (end_date == salary_table.enddate):
                salary_table_id = salary_table.id
                break

        salaries = [{'salary_id': salary.id,
                   'employeeid': salary.employeeid.id,
                   'salarytableid': salary.salarytableid.id,
                   'fine': salary.fine,
                   'reward': salary.reward} for salary in Salary.objects.filter(salarytableid=salary_table_id)]

        return json_format(code = 200, message = "Success", data = salaries)

class EditSalary(APIView):
    def post(self, request, format=None):
        data = request.data
        salary = Salary.objects.get(id=data['salary_id'])
        if "employee_id" in data.keys():
            employee = Employee.objects.get(id=data['employee_id'])
            salary.employeeid = employee
        if "fine" in data.keys():
            salary.fine = data['fine']
        if "reward" in data.keys():
            salary.reward = data['reward']
        salary.save()
        return json_format(code = 200, message = "Success")

class DeleteSalary(APIView):
    def post(self, request, format=None):
        data = request.data
        salary = Salary.objects.get(id=data['salary_id'])
        salary.delete()
        return json_format(code = 200, message = "Success")

class DeleteTax(APIView):
    def post(self, request, format=None):
        data = request.data
        tax = Tax.objects.get(id=data['tax_id'])
        tax.delete()
        return json_format(code = 200, message = "Success")

class EditTax(APIView):
    def post(self, request, format=None):
        data = request.data
        tax = Tax.objects.get(id=data['tax_id'])
        if "taxtype" in data.keys():
            tax.taxtype = data['taxtype']
        if "percentage" in data.keys():
            tax.percentage = data['percentage']
        tax.save()
        return json_format(code = 200, message = "Success")

class GetTax(APIView):
    def get(self, request, format=None):
        taxes = [{'tax_id': tax.id,
                   'taxtype': tax.taxtype,
                   'percentage': tax.percentage} for tax in Tax.objects.all()]

        return json_format(code = 200, message = "Success", data = taxes)

class DeleteLog(APIView):
    def post(self, request, format=None):
        data = request.data
        log = Log.objects.get(id=data['log_id'])
        log.delete()
        return json_format(code = 200, message = "Success")

class EditLog(APIView):
    def post(self, request, format=None):
        data = request.data
        log = Log.objects.get(id=data['log_id'])
        if "userid" in data.keys():
            user = User.objects.get(id=data['userid'])
            log.userid = user
        if "name" in data.keys():
            log.name = data['name']
        if "action" in data.keys():
            log.action = data['action']
        if "time" in data.keys():
            log.time = datetime.datetime.fromtimestamp(data['time'])
        log.save()
        return json_format(code = 200, message = "Success")

class GetLog(APIView):
    def get(self, request, format=None):
        logs = [{'log_id': log.id,
                   'userid': log.userid.id,
                   'name': log.name,
                   'action': log.action,
                   'time': log.time} for log in Log.objects.all()]

        return json_format(code = 200, message = "Success", data = logs)

class AddLog(APIView):
    def post(self, request, format=None):
        data = request.data
        logs_id = [log.id for log in Log.objects.all()]

        log = Log()
        while True:
            id = randomDigits(8, len(logs_id))
            if id not in logs_id:
                log.id = id
                break
        
        log.time = datetime.datetime.fromtimestamp(data['time'])
        log.name = data['name']
        log.action = data['action']

        user = User.objects.get(id=data['userid'])
        log.userid = user

        log.save()
        return json_format(code = 200, message = "Success")

class SummarySalaryTable(APIView):
    def get(self, request, format=None):
        salary_tables = [{'salary_table_id': salary_table.id,
                        'total': salary_table.total,
                        'note': salary_table.note,
                        'start_date': salary_table.startdate,
                        'end_date': salary_table.enddate} for salary_table in Salarytable.objects.all()]

        return json_format(code = 200, message = "Success", data = salary_tables)