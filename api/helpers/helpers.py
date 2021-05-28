import random
from ..models import *
import datetime
import numpy as np

def getProduct(productid = None):
    products = [product for product in Product.objects.all()]
    return_data = []
    for product in products:
        tmp = {}
        tmp['product_id'] = product.id
        tmp['partner_id'] = getPartner(product.partnerid.id)
        tmp['branch_id'] = getBranch(product.branchid.id)
        tmp['name'] = product.name
        tmp['ctrprice'] = product.ctrprice
        tmp['inprice'] = product.inprice
        tmp['outprice'] = product.outprice
        tmp['numinbranch'] = product.numinbranch
        if productid == product.id:
            return_data = tmp
            break
        return_data.append(tmp)

    return return_data

def getUser(userid = None):
        users = [user for user in User.objects.all()]
        type_acc = np.array(["Manager", "Chiefmanager", "Accountant", "Admin"])
        return_data = []
        for user in users:
            list1 = np.array([Manager.objects.filter(userid=user.id).count(), Chiefmanager.objects.filter(userid=user.id).count(), \
                        Accountant.objects.filter(userid=user.id).count(), Admin.objects.filter(userid=user.id).count()])
            account_type = type_acc[list1 != 0][0]
            tmp = {}
            tmp["user_id"] = user.id
            tmp["username"] = user.username
            tmp["password"] = user.password
            tmp["email"] = user.email
            tmp["address"] = user.address
            tmp["sex"] = user.sex
            tmp["type"] = account_type
            if userid == user.id:
                return_data = tmp
                break
            return_data.append(tmp)

        return return_data

def getPartner(partnerid):
    partners = [partner for partner in Partner.objects.all()]
    return_data = []
    for partner in partners:
        tmp = {}
        tmp["partner_id"] = partner.id
        tmp["partnername"] = partner.name
        tmp["taxid"] = partner.taxid
        tmp["desc"] = partner.desc
        tmp["address"] = partner.address
        tmp["email"] = partner.email
        tmp["phone"] = partner.phone
        if partnerid == partner.id:
            return_data = tmp
            break
        return_data.append(tmp)
    return return_data

def getBranch(branchid):
    if branchid is None:
        branchs = [{'branch_id': branch.id,
                    'branch_phone': branch.phone,
                    'branch_location': branch.location} for branch in Branch.objects.all()]
    else:
        branch =  Branch.objects.get(id=branchid)
        branchs = {'branch_id': branch.id,
                    'branch_phone': branch.phone,
                    'branch_location': branch.location}
    return branchs

def getDepartment(departmentid=None):
    if departmentid is not None:
        department = Department.objects.get(id=departmentid)
        departments = {'department_id': department.id,
                    'branch': getBranch(department.branchid.id),
                    'department_name': department.name,
                    'department_numofemployees': department.numofemployees} 
    else:
        departments = [{'department_id': department.id,
                        'branch': getBranch(department.branchid.id),
                        'department_name': department.name,
                        'department_numofemployees': department.numofemployees} for department in Department.objects.all()]
    return departments

def getEmployee(employeeid):
    if employeeid is not None:
        employee = Employee.objects.get(id=employeeid)
        employees = {'employee_id': employee.id,
                    'department_id': getDepartment(employee.departmentid.id),
                    'employee_name': employee.name,
                    'employee_taxid': getTax(employee.taxid.id),
                    'employee_phone': employee.phone,
                    'employee_email': employee.email,
                    'employee_address': employee.address,
                    'employee_sex': employee.sex,
                    'employee_exp': employee.exp,
                    'employee_salary': employee.salarydefault,
                    'employee_coef': employee.coef} 
    else:
        employees = [{'employee_id': employee.id,
                    'department_id': getDepartment(employee.departmentid.id),
                    'employee_name': employee.name,
                    'employee_taxid': getTax(employee.taxid.id),
                    'employee_phone': employee.phone,
                    'employee_email': employee.email,
                    'employee_address': employee.address,
                    'employee_sex': employee.sex,
                    'employee_exp': employee.exp,
                    'employee_salary': employee.salarydefault,
                    'employee_coef': employee.coef} for employee in Employee.objects.all()]
    return employees

def getSalary(salaryid=None):
    if salaryid is not None:
        salary = Salary.objects.get(id=salaryid)
        salaries = {'salary_id': salary.id,
                'employeeid': getEmployee(salary.employeeid.id),
                'salarytableid': salary.salarytableid.id,
                'fine': salary.fine,
                'reward': salary.reward}

    else:
        salaries = [{'salary_id': salary.id,
                'employeeid': getEmployee(salary.employeeid.id),
                'salarytableid': salary.salarytableid.id,
                'fine': salary.fine,
                'reward': salary.reward} for salary in Salary.objects.all()]
    return salaries

def getTax(taxid):
    if taxid is not None:
        tax = Tax.objects.get(id=taxid)
        taxes = {'tax_id': tax.id,
                   'taxtype': tax.taxtype,
                   'percentage': tax.percentage}
    else:
        taxes = [{'tax_id': tax.id,
                   'taxtype': tax.taxtype,
                   'percentage': tax.percentage} for tax in Tax.objects.all()]

    return taxes

def getReceipt(documentid = None):
    if documentid is not None:
        receipt = Receipt.objects.get(documentid__id=documentid)
        receipts = {'receipttype': receipt.receipttype,
                   'desc': receipt.desc,
                   'documentid': receipt.documentid.id}
    else:
        receipts = [{'receipttype': receipt.receipttype,
                   'desc': receipt.desc,
                   'documentid': receipt.documentid.id} for receipt in Receipt.objects.all()]

    return receipts