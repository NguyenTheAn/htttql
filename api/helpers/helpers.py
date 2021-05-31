import random
from ..models import *
import datetime
import numpy as np
from calendar import monthrange

WorkingDayPerMonth = 24

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
            if account_type == "Manager":
                tmp['branch'] = getBranch(Manager.objects.get(userid__id = user.id).branchid.id)
            elif account_type == "Accountant":
                tmp['branch'] = getBranch(Accountant.objects.get(userid__id = user.id).branchid.id)
                
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
                    'bankid' : employee.bankid,
                    'bankname' : employee.bankname,
                    'employee_address': employee.address,
                    'employee_sex': employee.sex,
                    'employee_exp': employee.exp,
                    'employee_salary': employee.salarydefault} 
    else:
        employees = [{'employee_id': employee.id,
                    'department_id': getDepartment(employee.departmentid.id),
                    'employee_name': employee.name,
                    'employee_taxid': getTax(employee.taxid.id),
                    'employee_phone': employee.phone,
                    'employee_email': employee.email,
                    'bankid' : employee.bankid,
                    'bankname' : employee.bankname,
                    'employee_address': employee.address,
                    'employee_sex': employee.sex,
                    'employee_exp': employee.exp,
                    'employee_salary': employee.salarydefault} for employee in Employee.objects.all()]
    return employees

def getSalary(salaryid=None):
    if salaryid is not None:
        salary = Salary.objects.get(id=salaryid)
        total = computeSalary(salary.employeeid.salarydefault,
                              salary.workingday,
                              WorkingDayPerMonth,
                              salary.fine,
                              salary.reward,
                              salary.employeeid.taxid.percentage/100)
        salaries = {'salary_id': salary.id,
                'employeeid': getEmployee(salary.employeeid.id),
                'salarytableid': salary.salarytableid.id,
                'fine': salary.fine,
                'reward': salary.reward,
                'workingday': salary.workingday,
                'total': total}

    else:
        salaries = [{'salary_id': salary.id,
                'employeeid': getEmployee(salary.employeeid.id),
                'salarytableid': salary.salarytableid.id,
                'fine': salary.fine,
                'reward': salary.reward,
                'workingday': salary.workingday,
                'total': computeSalary(salary.employeeid.salarydefault,
                                        salary.workingday,
                                        WorkingDayPerMonth,
                                        salary.fine,
                                        salary.reward,
                                        salary.employeeid.taxid.percentage/100)} for salary in Salary.objects.all()]
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
                   'documentid': getDocument(receipt.documentid.id)}
    else:
        receipts = [{'receipttype': receipt.receipttype,
                   'desc': receipt.desc,
                   'documentid': getDocument(receipt.documentid.id)} for receipt in Receipt.objects.all()]

    return receipts

def getBalancerec(balanceid = None):
    if balanceid is not None:
        balance = Balancerec.objects.get(id=balanceid)
        balances = {'id': balance.id,
                   'accountantuserid': balance.accountantuserid.userid.id,
                   'content': balance.content,
                   'amount': balance.amount,
                   'term': balance.term}
    else:
        balances = [{'id': balance.id,
                   'accountantuserid': balance.accountantuserid.userid.id,
                   'content': balance.content,
                   'amount': balance.amount,
                   'term': balance.term} for balance in Balancerec.objects.all()]

    return balances

def getLend(lendid = None):
    lendrecs = [lendrec for lendrec in Lendrec.objects.all()]
    redata = []
    for lendrec in lendrecs:
        tmp = dict()
        tmp['id'] = lendrec.id
        tmp["partnerid"] = getPartner(lendrec.partnerid.id)
        tmp['userid'] = getUser(lendrec.chiefmanageruserid.userid.id)
        tmp['desc'] = lendrec.desc
        tmp['amount'] = lendrec.amount
        tmp['remaining'] = lendrec.remaining
        tmp['time'] = lendrec.time.strftime("%d/%m/%Y")
        tmp['expired'] = lendrec.expired.strftime("%d/%m/%Y")
        tmp['interest_rate'] = lendrec.interest_rate

        if lendid == lendrec.id:
            redata = tmp
            break
        redata.append(tmp)
    return redata

def getLendPaying(lendpayingid = None):
    if lendpayingid is None:
        lendpayings = [{
            'id' : lendpaying.id,
            'lendrec' : getLend(lendpaying.lendrecid.id),
            'interest_amount' : lendpaying.interestamount,
            'payingamount' : lendpaying.payingamount,
            'time' : lendpaying.time.strftime("%d/%m/%Y"),
            'payment' : lendpaying.payment
        } for lendpaying in LendPaying.objects.all()]
    else:
        lendpaying = LendPaying.objects.get(id = lendpayingid)
        lendpayings = {
            'id' : lendpaying.id,
            'lendrec' : getLend(lendpaying.lendrecid.id),
            'interest_amount' : lendpaying.interestamount,
            'payingamount' : lendpaying.payingamount,
            'time' : lendpaying.time.strftime("%d/%m/%Y"),
            'payment' : lendpaying.payment
        }
    return lendpayings

def getLoan(loanid = None):
    loanrecs = [loanrec for loanrec in Loanrec.objects.all()]
    redata = []
    for loanrec in loanrecs:
        tmp = dict()
        tmp['id'] = loanrec.id
        tmp['userid'] = loanrec.chiefmanageruserid.userid.id
        tmp['desc'] = loanrec.desc
        tmp['amount'] = loanrec.amount
        tmp['remaining'] = loanrec.remaining
        tmp['time'] = loanrec.time.strftime("%d/%m/%Y")
        tmp['expired'] = loanrec.expired.strftime("%d/%m/%Y")
        tmp['interest_rate'] = loanrec.interest_rate

        if loanid == loanrec.id:
            redata = tmp
            break
        redata.append(tmp)
    return redata

def getLoanPaying(loanpayingid = None):
    if loanpayingid is None:
        loanpayings = [{
            'id' : loanpaying.id,
            'partner' : getPartner(loanpaying.loanrecid.partnerid.id),
            'lendrec' : getLend(loanpaying.loanrecid.id),
            'interest_amount' : loanpaying.interestamount,
            'payingamount' : loanpaying.payingamount,
            'time' : loanpaying.time.strftime("%d/%m/%Y"),
            'payment' : loanpaying.payment
        } for loanpaying in LoanPaying.objects.all()]
    else:
        loanpaying = LoanPaying.objects.get(id = loanpayingid)
        loanpayings = {
            'id' : loanpaying.id,
            'partner' : getPartner(loanpaying.loanrecid.partnerid.id),
            'lendrec' : getLend(loanpaying.loanrecid.id),
            'interest_amount' : loanpaying.interestamount,
            'payingamount' : loanpaying.payingamount,
            'time' : loanpaying.time.strftime("%d/%m/%Y"),
            'payment' : loanpaying.payment
        }
    return loanpayings

def getSalaryTable(table_date):

    m, y = [int(i) for i in table_date.split("/")]
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
                'employeeid': getEmployee(salary.employeeid.id),
                'salarytableid': salary.salarytableid.id,
                'fine': salary.fine,
                'reward': salary.reward,
                'workingday': salary.workingday,
                'total': computeSalary(salary.employeeid.salarydefault,
                                        salary.workingday,
                                        WorkingDayPerMonth,
                                        salary.fine,
                                        salary.reward,
                                        salary.employeeid.taxid.percentage/100)} for salary in Salary.objects.filter(salarytableid=salary_table_id)]

    return salaries


def getSalaryByEmployee(employeeid):
    salaries = [{'salary_id': salary.id,
                'employeeid': getEmployee(salary.employeeid.id),
                'salarytableid': salary.salarytableid.id,
                'fine': salary.fine,
                'reward': salary.reward,
                'workingday': salary.workingday,
                'total': computeSalary(salary.employeeid.salarydefault,
                                        salary.workingday,
                                        WorkingDayPerMonth,
                                        salary.fine,
                                        salary.reward,
                                        salary.employeeid.taxid.percentage/100)} for salary in Salary.objects.filter(employeeid__id=employeeid)]

    return salaries
    
def getSalaryByDepartment(departmentid):
    salaries = [{'salary_id': salary.id,
                'employeeid': getEmployee(salary.employeeid.id),
                'salarytableid': salary.salarytableid.id,
                'fine': salary.fine,
                'reward': salary.reward,
                'workingday': salary.workingday,
                'total': computeSalary(salary.employeeid.salarydefault,
                                        salary.workingday,
                                        WorkingDayPerMonth,
                                        salary.fine,
                                        salary.reward,
                                        salary.employeeid.taxid.percentage/100)} for salary in Salary.objects.filter(employeeid__departmentid__id=departmentid)]

    return salaries

def salaryStatisticByBranch(branchid):
    return_list = dict()
    time_now = datetime.datetime.now()
    y, m = time_now.year, time_now.month
    max = -1
    min = 99999
    mintype = None
    maxtype = None
    tmp_ = {}
    for i in range(1, m+1):
        sum = 0
        salaries = Salary.objects.filter(employeeid__departmentid__branchid__id = branchid, salarytableid__startdate__year = y, salarytableid__startdate__month = i)
        for salary in salaries:
            total = computeSalary(salary.employeeid.salarydefault,
                                        salary.workingday,
                                        WorkingDayPerMonth,
                                        salary.fine,
                                        salary.reward,
                                        salary.employeeid.taxid.percentage/100)
            sum += total
        tmp_["%.2d/%.4d" % (i, y)] = sum
        if max < sum:
            max = sum
            maxtype = "%.2d/%.4d" % (i, y)
        if min > sum:
            min = sum
            mintype = "%.2d/%.4d" % (i, y)
    return_list["statistic"] = [{"date" : k, "value" : tmp_[k]} for k in tmp_.keys()]        
    return_list['max'] = {'type' : maxtype,
                        'value' : max}
    return_list['min'] = {'type' : mintype,
                        'value' : min}
    return return_list

def getInterestInBranch(branchid, month, year):
    # balance = Balancerec.objects.get(accountantuserid__branchid__id = branchid)
    salaries = Salary.objects.filter(employeeid__departmentid__branchid__id = branchid, salarytableid__startdate__year = year, salarytableid__startdate__month = month)
    reciepts = Receipt.objects.filter(documentid__accountantuserid__branchid__id = branchid, documentid__time__year = year, documentid__time__month = month)
    buybills = BuyBill.objects.filter(branchid__id = branchid, documentid__time__year = year, documentid__time__month = month)
    sellbills = SellBill.objects.filter(branchid__id = branchid, documentid__time__year = year, documentid__time__month = month)
    data = {}
    interest = 0
    s = 0
    tncn = 0
    for salary in salaries:
        total = computeSalary(salary.employeeid.salarydefault,
                                        salary.workingday,
                                        WorkingDayPerMonth,
                                        salary.fine,
                                        salary.reward,
                                        salary.employeeid.taxid.percentage/100)
        tncn += (salary.employeeid.taxid.percentage/100)*total
        interest -= total
        s += total
    data['salary'] = s
    s = 0
    for reciept in reciepts:
        interest -= reciept.documentid.amount
        s += reciept.documentid.amount
    data['reciept'] = s
    s = 0
    for buybill in buybills:
        interest -= buybill.documentid.amount
        s -= buybill.documentid.amount
    data['buybill'] = s
    s = 0
    gtgt = 0
    for sellbill in sellbills:
        interest += sellbill.documentid.amount
        s += sellbill.documentid.amount
        tax_pay = sellbill.documentid.amount * sellbill.taxid.percentage / 100.0
        gtgt += tax_pay
    data['sellbill'] = s
    data['gtgt'] = gtgt
    data['tncn'] = tncn
    data['interest'] = interest
    return data

def getDocument(documentid):
    document = Document.objects.get(id = documentid)
    data = {
        "id" : document.id,
        "user" : getUser(document.accountantuserid.userid.id),
        "name" : document.name,
        "type" : document.type,
        "content" : document.content,
        "amount" : document.amount,
        "time" : document.time,
    }
    return data

def getTaxStatisticByBranch(taxid, branchid):
    tax = Tax.objects.get(id=taxid)
    return_list = dict()
    return_list["tax"] = getTax(tax.id)
    max = -1
    min = 99999
    mintype = None
    maxtype = None
    tmp_ = {}
    if "TNCN" in tax.taxtype:
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        for i in range(1, m+1):
            sum = 0
            salaries = Salary.objects.filter(employeeid__departmentid__branchid__id = branchid, salarytableid__startdate__year = y, salarytableid__startdate__month = i,
                                            employeeid__taxid__id = tax.id)
            for salary in salaries:
                total = computeSalary(salary.employeeid.salarydefault,
                                        salary.workingday,
                                        WorkingDayPerMonth,
                                        salary.fine,
                                        salary.reward,
                                        salary.employeeid.taxid.percentage/100)
                tax_pay = total * float(tax.percentage) / 100.0
                sum += tax_pay
            tmp_["%.2d/%.4d" % (i, y)] = sum

    if "GTGT" in tax.taxtype:
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        for i in range(1, m+1):
            sum = 0
            sellbills = SellBill.objects.filter(branchid__id = branchid, documentid__time__year = y, documentid__time__month = i, taxid__id = tax.id)
            for sellbill in sellbills:
                tax_pay = sellbill.documentid.amount * float(tax.percentage) / 100.0
                sum += tax_pay
            tmp_["%.2d/%.4d" % (i, y)] = sum
    if "TNDN" in tax.taxtype:
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        for i in range(1, m+1):
            interest = getInterestInBranch(branchid, i, y)['interest']
            if interest > 0:
                sum = interest * float(tax.percentage) / 100.0
            else:
                sum = 0
            tmp_["%.2d/%.4d" % (i, y)] = sum
    return_list["statistic"] = [{"date" : k, "value" : tmp_[k]} for k in tmp_.keys()]
    for k in tmp_.keys():
        if tmp_[k] > max:
            max = tmp_[k]
            maxtype = k
        if tmp_[k] < min:
            min = tmp_[k]
            mintype = k
    if max < sum:
        max = sum
        maxtype = tax.taxtype
    if min > sum:
        min = sum
        mintype = tax.taxtype
        
    return_list['max'] = {'type' : maxtype,
                        'value' : max}
    return_list['min'] = {'type' : mintype,
                        'value' : min}
    return return_list

def getAllTaxByBranch(branchid):
    taxs = Tax.objects.all()
    return_list = dict()
    time_now = datetime.datetime.now()
    y, m = time_now.year, time_now.month
    max = -1
    min = 99999
    mintype = None
    maxtype = None
    tmp_ = {}
    for i in range(1, m+1):
        total = 0
        for tax in taxs:
            if "TNCN" in tax.taxtype:
                sum = 0
                salaries = Salary.objects.filter(employeeid__departmentid__branchid__id = branchid, salarytableid__startdate__year = y, salarytableid__startdate__month = i,
                                                employeeid__taxid__id = tax.id)
                for salary in salaries:
                    total_ = computeSalary(salary.employeeid.salarydefault,
                                        salary.workingday,
                                        WorkingDayPerMonth,
                                        salary.fine,
                                        salary.reward,
                                        salary.employeeid.taxid.percentage/100)
                    tax_pay = total_ * float(tax.percentage) / 100.0
                    sum += tax_pay
                total += sum

            if "GTGT" in tax.taxtype:
                sum = 0
                sellbills = SellBill.objects.filter(branchid__id = branchid, documentid__time__year = y, documentid__time__month = i, taxid__id = tax.id)
                for sellbill in sellbills:
                    tax_pay = sellbill.documentid.amount * float(tax.percentage) / 100.0
                    sum += tax_pay
                total += sum
            if "TNDN" in tax.taxtype:
                interest = getInterestInBranch(branchid, i, y)['interest']
                if interest > 0:
                    sum = interest * float(tax.percentage) / 100.0
                else:
                    sum = 0
                total += sum
        if max < total:
            max = total
            maxtype = "%.2d/%.4d" % (i, y)
        if min > total:
            min = total
            mintype = "%.2d/%.4d" % (i, y)

        tmp_["%.2d/%.4d" % (i, y)] = total
    return_list["statistic"] = [{"date" : k, "value" : tmp_[k]} for k in tmp_.keys()]
    return_list['max'] = {'type' : maxtype,
                        'value' : max}
    return_list['min'] = {'type' : mintype,
                        'value' : min}
    return return_list

def computeSalary(salaryDefault, workingDay, workingDayPerMonth, fine, reward, tax):
    tota = (salaryDefault * workingDay / workingDayPerMonth  + reward - fine)
    return tota * (1 - tax)