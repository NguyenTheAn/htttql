# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remov` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# doi gen id tu nho den lon

# branch name -> phone
# thêm admin
# product in_out price and date time
# LenRec thêm lãi
# Accountant bỏ team
# bill time dung .now

class Accountant(models.Model):
    created = models.DateField(db_column='Created', blank=True, null=True)  # Field name made lowercase.
    userid = models.OneToOneField('User', models.CASCADE, db_column='UserID', primary_key=True)  # Field name made lowercase.
    branchid = models.ForeignKey('Branch', models.CASCADE, db_column='BranchID')  # Field name made lowercase.

    class Meta:
        db_table = 'accountant'


class Balancerec(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    accountantuserid = models.ForeignKey(Accountant, models.CASCADE, db_column='AccountantUserID')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.

    class Meta:
        db_table = 'balancerec'

class Branch(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    phone = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'branch'


class Chiefmanager(models.Model):
    userid = models.OneToOneField('User', models.CASCADE, db_column='UserID', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'chiefmanager'

class Admin(models.Model):
    userid = models.OneToOneField('User', models.CASCADE, db_column='UserID', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'admin'

class Department(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    branchid = models.ForeignKey(Branch, models.CASCADE, db_column='BranchID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numofemployees = models.IntegerField(db_column='NumOfEmployees')  # Field name made lowercase.

    class Meta:
        db_table = 'department'


class Document(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    accountantuserid = models.ForeignKey(Accountant, models.CASCADE, db_column='AccountantUserID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', default= 0)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'document'


class Employee(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    departmentid = models.ForeignKey(Department, models.CASCADE, db_column='DepartmentID')  # Field name made lowercase.
    taxid = models.ForeignKey("Tax", models.CASCADE, db_column='TaxID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=255, blank=True, null=True)  # Field name made lowercase.
    exp = models.FloatField(db_column='Exp')  # Field name made lowercase.
    salarydefault = models.FloatField(db_column='Salary', blank=True, null=True)  # Field name made lowercase.
    coef = models.FloatField(db_column='Coef', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'employee'


class Investmentrec(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    chiefmanageruserid = models.ForeignKey(Chiefmanager, models.CASCADE, db_column='ChiefManagerUserID')  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.

    class Meta:
        db_table = 'investmentrec'


class Lendrec(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    partnerid = models.ForeignKey('Partner', models.CASCADE, db_column='PartnerID')  # Field name made lowercase.
    chiefmanageruserid = models.ForeignKey(Chiefmanager, models.CASCADE, db_column='ChiefManagerUserID')  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    interest_rate = models.FloatField(db_column='InterestRate', blank=True, null=True) 

    class Meta:
        db_table = 'lendrec'


class Loanrec(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    chiefmanageruserid = models.ForeignKey(Chiefmanager, models.CASCADE, db_column='ChiefManagerUserID')  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    interest_rate = models.FloatField(db_column='InterestRate', blank=True, null=True) 

    class Meta:
        db_table = 'loanrec'

class Partner(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taxid = models.CharField(db_column='TaxId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'partner'


class Product(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    branchid = models.ForeignKey(Branch, models.CASCADE, db_column='BranchID')  # Field name made lowercase.
    partnerid = models.ForeignKey(Partner, models.CASCADE, db_column='PartnerID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ctrprice = models.FloatField(db_column='CtrPrice', blank=True, null=True)  # Field name made lowercase.
    inprice = models.FloatField(db_column='InPrice', blank=True, null=True)  # Field name made lowercase.
    outprice = models.FloatField(db_column='OutPrice', blank=True, null=True)  # Field name made lowercase.
    numinbranch = models.IntegerField(db_column='NumInBranch', blank=True, null=True, default=0)  # Field name made lowercase.

    class Meta:
        db_table = 'product'


class ProductSellBill(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)
    productid = models.ForeignKey(Product, models.CASCADE, db_column='ProductID')  # Field name made lowercase.
    sellbilldocumentid = models.ForeignKey('sellBill', models.CASCADE, db_column='SellBillDocumentID')  # Field name made lowercase.
    numinbill = models.IntegerField(db_column='NumberInBill', blank=True, null=True)

    class Meta:
        db_table = 'product_sell_bill'
        unique_together = (('productid', 'sellbilldocumentid'),)

class ProductBuyBill(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)
    productid = models.ForeignKey(Product, models.CASCADE, db_column='ProductID')  # Field name made lowercase.
    buybilldocumentid = models.ForeignKey('BuyBill', models.CASCADE, db_column='BuyBillDocumentID')  # Field name made lowercase.
    numinbill = models.IntegerField(db_column='NumberInBill', blank=True, null=True)

    class Meta:
        db_table = 'product_buy_bill'
        unique_together = (('productid', 'buybilldocumentid'),)

class BuyBill(models.Model):
    branchid = models.ForeignKey('Branch', models.CASCADE, db_column='BranchID')
    documentid = models.OneToOneField('Document', models.CASCADE, db_column='DocumentID', primary_key=True)  # Field name made lowercase.
    payment = models.CharField(db_column='PaymentMethod', max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'buy_bill'

class SellBill(models.Model):
    branchid = models.ForeignKey('Branch', models.CASCADE, db_column='BranchID')
    customer = models.CharField(db_column='Customer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    documentid = models.OneToOneField('Document', models.CASCADE, db_column='DocumentID', primary_key=True)  # Field name made lowercase.
    taxid = models.ForeignKey('Tax', models.CASCADE, db_column='TaxID')  # Field name made lowercase.
    cusaddress = models.CharField(db_column='CusAddress', max_length=255, blank=True, null=True)
    payment = models.CharField(db_column='PaymentMethod', max_length=255, blank=True, null=True)
    cusphone = models.CharField(db_column='CusPhone', max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'sell_bill'

class Receipt(models.Model):
    receipttype = models.CharField(db_column='ReceiptType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    documentid = models.OneToOneField(Document, models.CASCADE, db_column='DocumentID', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'receipt'


class Report(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    accountantuserid = models.ForeignKey(Accountant, models.CASCADE, db_column='AccountantUserID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sum = models.FloatField(db_column='Sum')  # Field name made lowercase.

    class Meta:
        db_table = 'report'


class Salary(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    employeeid = models.ForeignKey(Employee, models.CASCADE, db_column='EmployeeID')  # Field name made lowercase.
    salarytableid = models.ForeignKey('Salarytable', models.CASCADE, db_column='SalaryTableID')  # Field name made lowercase.
    fine = models.FloatField(db_column='Fine', blank=True, null=True)  # Field name made lowercase.
    reward = models.FloatField(db_column='Reward')  # Field name made lowercase.

    class Meta:
        db_table = 'salary'


class Salarytable(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    total = models.FloatField(db_column='Total')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)

    class Meta:
        db_table = 'salarytable'

class Tax(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)
    taxtype = models.CharField(db_column='TaxType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    percentage = models.FloatField(db_column='Percentage')  # Field name made lowercase.

    class Meta:
        db_table = 'tax'


class User(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    username = models.CharField(db_column='Username', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'user'

class Manager(models.Model):
    created = models.DateField(db_column='Created', blank=True, null=True)  # Field name made lowercase.
    userid = models.OneToOneField(User, models.CASCADE, db_column='UserID', primary_key=True)  # Field name made lowercase.
    branchid = models.ForeignKey(Branch, models.CASCADE, db_column='BranchID')  # Field name made lowercase.

    class Meta:
        db_table = 'manager'


class Statisticrec(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    chiefmanageruserid = models.ForeignKey(Chiefmanager, models.CASCADE, db_column='ChiefManagerUserID')  # Field name made lowercase.
    manageruserid = models.ForeignKey(Manager, models.CASCADE, db_column='ManagerUserID')  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    num = models.FloatField(db_column='Num')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'statisticrec'

class Summary(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    statisticrecid = models.ForeignKey(Statisticrec, models.CASCADE, db_column='StatisticRecID')  # Field name made lowercase.
    taxid = models.ForeignKey("Tax", models.CASCADE, db_column='TaxID')  # Field name made lowercase.
    term = models.CharField(db_column='Term', max_length=255, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=255, blank=True, null=True)  # Field name made lowercase.
    detail = models.CharField(db_column='Detail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    balance = models.FloatField(db_column='Balance')  # Field name made lowercase.
    tax = models.FloatField(db_column='Tax')  # Field name made lowercase.

    class Meta:
        db_table = 'summary'