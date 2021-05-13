# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accountant(models.Model):
    created = models.DateField(db_column='Created', blank=True, null=True)  # Field name made lowercase.
    team = models.IntegerField(db_column='Team')  # Field name made lowercase.
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.
    branchid = models.ForeignKey('Branch', models.DO_NOTHING, db_column='BranchID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accountant'


class Balancerec(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    accountantuserid = models.ForeignKey(Accountant, models.DO_NOTHING, db_column='AccountantUserID')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'balancerec'


class Bill(models.Model):
    billtype = models.CharField(db_column='BillType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tax = models.TextField(db_column='Tax')  # Field name made lowercase. This field type is a guess.
    documentid = models.OneToOneField('Document', models.DO_NOTHING, db_column='DocumentID', primary_key=True)  # Field name made lowercase.
    partnerid = models.ForeignKey('Partner', models.DO_NOTHING, db_column='PartnerID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bill'


class Branch(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'branch'


class Chiefmanager(models.Model):
    cardid = models.CharField(db_column='CardID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chiefmanager'


class Department(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    branchid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BranchID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numofemployees = models.IntegerField(db_column='NumOfEmployees')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'department'


class Document(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    accountantuserid = models.ForeignKey(Accountant, models.DO_NOTHING, db_column='AccountantUserID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'document'


class Employee(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    departmentid = models.ForeignKey(Department, models.DO_NOTHING, db_column='DepartmentID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=255, blank=True, null=True)  # Field name made lowercase.
    exp = models.FloatField(db_column='Exp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employee'


class Investmentrec(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    chiefmanageruserid = models.ForeignKey(Chiefmanager, models.DO_NOTHING, db_column='ChiefManagerUserID')  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'investmentrec'


class Lendrec(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    partnerid = models.ForeignKey('Partner', models.DO_NOTHING, db_column='PartnerID')  # Field name made lowercase.
    chiefmanageruserid = models.ForeignKey(Chiefmanager, models.DO_NOTHING, db_column='ChiefManagerUserID')  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lendrec'


class Loanrec(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    chiefmanageruserid = models.ForeignKey(Chiefmanager, models.DO_NOTHING, db_column='ChiefManagerUserID')  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'loanrec'


class Manager(models.Model):
    created = models.DateField(db_column='Created', blank=True, null=True)  # Field name made lowercase.
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.
    branchid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BranchID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'manager'


class Partner(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taxid = models.CharField(db_column='TaxId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partner'


class Product(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    branchid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BranchID')  # Field name made lowercase.
    partnerid = models.ForeignKey(Partner, models.DO_NOTHING, db_column='PartnerID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numinbranch = models.IntegerField(db_column='NumInBranch')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product'


class ProductBill(models.Model):
    productid = models.OneToOneField(Product, models.DO_NOTHING, db_column='ProductID', primary_key=True)  # Field name made lowercase.
    billdocumentid = models.ForeignKey(Bill, models.DO_NOTHING, db_column='BillDocumentID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product_bill'
        unique_together = (('productid', 'billdocumentid'),)


class Receipt(models.Model):
    receipttype = models.CharField(db_column='ReceiptType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    documentid = models.OneToOneField(Document, models.DO_NOTHING, db_column='DocumentID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'receipt'


class Report(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    accountantuserid = models.ForeignKey(Accountant, models.DO_NOTHING, db_column='AccountantUserID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sum = models.FloatField(db_column='Sum')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'report'


class Salary(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    employeeid = models.ForeignKey(Employee, models.DO_NOTHING, db_column='EmployeeID')  # Field name made lowercase.
    salarytableid = models.ForeignKey('Salarytable', models.DO_NOTHING, db_column='SalaryTableID')  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.
    adding = models.FloatField(db_column='Adding')  # Field name made lowercase.
    deducting = models.FloatField(db_column='Deducting')  # Field name made lowercase.
    sum = models.FloatField(db_column='Sum')  # Field name made lowercase.
    coef = models.FloatField(db_column='Coef')  # Field name made lowercase.
    reward = models.FloatField(db_column='Reward')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'salary'


class Salarytable(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    accountantuserid = models.ForeignKey(Accountant, models.DO_NOTHING, db_column='AccountantUserID')  # Field name made lowercase.
    total = models.FloatField(db_column='Total')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'salarytable'


class Statisticrec(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    chiefmanageruserid = models.ForeignKey(Chiefmanager, models.DO_NOTHING, db_column='ChiefManagerUserID')  # Field name made lowercase.
    manageruserid = models.ForeignKey(Manager, models.DO_NOTHING, db_column='ManagerUserID')  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    num = models.FloatField(db_column='Num')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'statisticrec'


class Summary(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    statisticrecid = models.ForeignKey(Statisticrec, models.DO_NOTHING, db_column='StatisticRecID')  # Field name made lowercase.
    term = models.CharField(db_column='Term', max_length=255, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=255, blank=True, null=True)  # Field name made lowercase.
    detail = models.CharField(db_column='Detail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    balance = models.FloatField(db_column='Balance')  # Field name made lowercase.
    tax = models.FloatField(db_column='Tax')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'summary'


class Taxinvoice(models.Model):
    taxtype = models.CharField(db_column='TaxType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    percentage = models.FloatField(db_column='Percentage')  # Field name made lowercase.
    attachedto = models.CharField(db_column='AttachedTo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    documentid = models.OneToOneField(Document, models.DO_NOTHING, db_column='DocumentID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'taxinvoice'


class User(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    username = models.CharField(db_column='Username', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'
