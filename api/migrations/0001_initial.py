# Generated by Django 3.0.5 on 2021-05-30 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('phone', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('location', models.CharField(blank=True, db_column='Location', max_length=255, null=True)),
            ],
            options={
                'db_table': 'branch',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('numofemployees', models.IntegerField(db_column='NumOfEmployees')),
                ('branchid', models.ForeignKey(db_column='BranchID', on_delete=django.db.models.deletion.CASCADE, to='api.Branch')),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('type', models.CharField(blank=True, db_column='Type', max_length=255, null=True)),
                ('content', models.CharField(blank=True, db_column='Content', max_length=255, null=True)),
                ('amount', models.FloatField(db_column='Amount', default=0)),
                ('time', models.DateField(blank=True, db_column='Time', null=True)),
            ],
            options={
                'db_table': 'document',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('bankid', models.CharField(blank=True, db_column='BankID', max_length=255, null=True)),
                ('bankname', models.CharField(blank=True, db_column='BankName', max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=255, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=255, null=True)),
                ('address', models.CharField(blank=True, db_column='Address', max_length=255, null=True)),
                ('sex', models.CharField(blank=True, db_column='Sex', max_length=255, null=True)),
                ('exp', models.FloatField(db_column='Exp')),
                ('salarydefault', models.FloatField(blank=True, db_column='Salary', null=True)),
                ('coef', models.FloatField(blank=True, db_column='Coef', null=True)),
                ('departmentid', models.ForeignKey(db_column='DepartmentID', on_delete=django.db.models.deletion.CASCADE, to='api.Department')),
            ],
            options={
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('taxid', models.CharField(blank=True, db_column='TaxId', max_length=255, null=True)),
                ('address', models.CharField(blank=True, db_column='Address', max_length=255, null=True)),
                ('desc', models.CharField(blank=True, db_column='Desc', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=255, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=255, null=True)),
            ],
            options={
                'db_table': 'partner',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('ctrprice', models.FloatField(blank=True, db_column='CtrPrice', null=True)),
                ('inprice', models.FloatField(blank=True, db_column='InPrice', null=True)),
                ('outprice', models.FloatField(blank=True, db_column='OutPrice', null=True)),
                ('numinbranch', models.IntegerField(blank=True, db_column='NumInBranch', default=0, null=True)),
                ('branchid', models.ForeignKey(db_column='BranchID', on_delete=django.db.models.deletion.CASCADE, to='api.Branch')),
                ('partnerid', models.ForeignKey(db_column='PartnerID', on_delete=django.db.models.deletion.CASCADE, to='api.Partner')),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Salarytable',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('total', models.FloatField(db_column='Total')),
                ('note', models.CharField(blank=True, db_column='Note', max_length=255, null=True)),
                ('startdate', models.DateField(blank=True, db_column='StartDate', null=True)),
                ('enddate', models.DateField(blank=True, db_column='EndDate', null=True)),
            ],
            options={
                'db_table': 'salarytable',
            },
        ),
        migrations.CreateModel(
            name='Statisticrec',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('time', models.DateField(blank=True, db_column='Time', null=True)),
                ('num', models.FloatField(db_column='Num')),
                ('title', models.CharField(blank=True, db_column='Title', max_length=255, null=True)),
            ],
            options={
                'db_table': 'statisticrec',
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('taxtype', models.CharField(blank=True, db_column='TaxType', max_length=255, null=True)),
                ('percentage', models.FloatField(db_column='Percentage')),
            ],
            options={
                'db_table': 'tax',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, db_column='Username', max_length=255, null=True, unique=True)),
                ('password', models.CharField(blank=True, db_column='Password', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=255, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=255, null=True)),
                ('address', models.CharField(blank=True, db_column='Address', max_length=255, null=True)),
                ('sex', models.CharField(blank=True, db_column='Sex', max_length=255, null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Accountant',
            fields=[
                ('created', models.DateField(blank=True, db_column='Created', null=True)),
                ('userid', models.OneToOneField(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.User')),
                ('branchid', models.ForeignKey(db_column='BranchID', on_delete=django.db.models.deletion.CASCADE, to='api.Branch')),
            ],
            options={
                'db_table': 'accountant',
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('userid', models.OneToOneField(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.User')),
            ],
            options={
                'db_table': 'admin',
            },
        ),
        migrations.CreateModel(
            name='BuyBill',
            fields=[
                ('documentid', models.OneToOneField(db_column='DocumentID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.Document')),
                ('payment', models.CharField(blank=True, db_column='PaymentMethod', max_length=255, null=True)),
                ('branchid', models.ForeignKey(db_column='BranchID', on_delete=django.db.models.deletion.CASCADE, to='api.Branch')),
            ],
            options={
                'db_table': 'buy_bill',
            },
        ),
        migrations.CreateModel(
            name='Chiefmanager',
            fields=[
                ('userid', models.OneToOneField(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.User')),
            ],
            options={
                'db_table': 'chiefmanager',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('created', models.DateField(blank=True, db_column='Created', null=True)),
                ('userid', models.OneToOneField(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.User')),
                ('branchid', models.ForeignKey(db_column='BranchID', on_delete=django.db.models.deletion.CASCADE, to='api.Branch')),
            ],
            options={
                'db_table': 'manager',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('receipttype', models.CharField(blank=True, db_column='ReceiptType', max_length=255, null=True)),
                ('desc', models.CharField(blank=True, db_column='Desc', max_length=255, null=True)),
                ('documentid', models.OneToOneField(db_column='DocumentID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.Document')),
            ],
            options={
                'db_table': 'receipt',
            },
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('term', models.CharField(blank=True, db_column='Term', max_length=255, null=True)),
                ('state', models.CharField(blank=True, db_column='State', max_length=255, null=True)),
                ('detail', models.CharField(blank=True, db_column='Detail', max_length=255, null=True)),
                ('balance', models.FloatField(db_column='Balance')),
                ('tax', models.FloatField(db_column='Tax')),
                ('statisticrecid', models.ForeignKey(db_column='StatisticRecID', on_delete=django.db.models.deletion.CASCADE, to='api.Statisticrec')),
                ('taxid', models.ForeignKey(db_column='TaxID', on_delete=django.db.models.deletion.CASCADE, to='api.Tax')),
            ],
            options={
                'db_table': 'summary',
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('fine', models.FloatField(blank=True, db_column='Fine', null=True)),
                ('reward', models.FloatField(db_column='Reward')),
                ('workingday', models.IntegerField(db_column='workingday')),
                ('employeeid', models.ForeignKey(db_column='EmployeeID', on_delete=django.db.models.deletion.CASCADE, to='api.Employee')),
                ('salarytableid', models.ForeignKey(db_column='SalaryTableID', on_delete=django.db.models.deletion.CASCADE, to='api.Salarytable')),
            ],
            options={
                'db_table': 'salary',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='name', max_length=255, null=True)),
                ('action', models.CharField(blank=True, db_column='action', max_length=255, null=True)),
                ('time', models.DateField(blank=True, db_column='Time', null=True)),
                ('userid', models.ForeignKey(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
            options={
                'db_table': 'log',
            },
        ),
        migrations.CreateModel(
            name='Loanrec',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('desc', models.CharField(blank=True, db_column='Desc', max_length=255, null=True)),
                ('amount', models.FloatField(db_column='Amount')),
                ('remaining', models.FloatField(db_column='RemainingAmount')),
                ('time', models.DateField(blank=True, db_column='Time', null=True)),
                ('expired', models.DateField(blank=True, db_column='expired', null=True)),
                ('interest_rate', models.FloatField(blank=True, db_column='InterestRate', null=True)),
                ('partnerid', models.ForeignKey(db_column='PartnerID', on_delete=django.db.models.deletion.CASCADE, to='api.Partner')),
                ('chiefmanageruserid', models.ForeignKey(db_column='ChiefManagerUserID', on_delete=django.db.models.deletion.CASCADE, to='api.Chiefmanager')),
            ],
            options={
                'db_table': 'loanrec',
            },
        ),
        migrations.CreateModel(
            name='LoanPaying',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('interestamount', models.FloatField(blank=True, db_column='InterestAmount', null=True)),
                ('payingamount', models.FloatField(blank=True, db_column='PayingAmount', null=True)),
                ('time', models.DateField(blank=True, db_column='Time', null=True)),
                ('payment', models.CharField(blank=True, db_column='PaymentMethod', max_length=255, null=True)),
                ('loanrecid', models.ForeignKey(db_column='Loanrecid', on_delete=django.db.models.deletion.CASCADE, to='api.Loanrec')),
            ],
            options={
                'db_table': 'loanpaying',
            },
        ),
        migrations.CreateModel(
            name='Lendrec',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('desc', models.CharField(blank=True, db_column='Desc', max_length=255, null=True)),
                ('amount', models.FloatField(db_column='Amount')),
                ('remaining', models.FloatField(db_column='RemainingAmount')),
                ('time', models.DateField(blank=True, db_column='Time', null=True)),
                ('expired', models.DateField(blank=True, db_column='expired', null=True)),
                ('interest_rate', models.FloatField(blank=True, db_column='InterestRate', null=True)),
                ('partnerid', models.ForeignKey(db_column='PartnerID', on_delete=django.db.models.deletion.CASCADE, to='api.Partner')),
                ('chiefmanageruserid', models.ForeignKey(db_column='ChiefManagerUserID', on_delete=django.db.models.deletion.CASCADE, to='api.Chiefmanager')),
            ],
            options={
                'db_table': 'lendrec',
            },
        ),
        migrations.CreateModel(
            name='LendPaying',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('interestamount', models.FloatField(blank=True, db_column='InterestAmount', null=True)),
                ('payingamount', models.FloatField(blank=True, db_column='PayingAmount', null=True)),
                ('time', models.DateField(blank=True, db_column='Time', null=True)),
                ('payment', models.CharField(blank=True, db_column='PaymentMethod', max_length=255, null=True)),
                ('lendrecid', models.ForeignKey(db_column='Lendrecid', on_delete=django.db.models.deletion.CASCADE, to='api.Lendrec')),
            ],
            options={
                'db_table': 'lendpaying',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='taxid',
            field=models.ForeignKey(db_column='TaxID', on_delete=django.db.models.deletion.CASCADE, to='api.Tax'),
        ),
        migrations.AddField(
            model_name='statisticrec',
            name='chiefmanageruserid',
            field=models.ForeignKey(db_column='ChiefManagerUserID', on_delete=django.db.models.deletion.CASCADE, to='api.Chiefmanager'),
        ),
        migrations.AddField(
            model_name='statisticrec',
            name='manageruserid',
            field=models.ForeignKey(db_column='ManagerUserID', on_delete=django.db.models.deletion.CASCADE, to='api.Manager'),
        ),
        migrations.CreateModel(
            name='SellBill',
            fields=[
                ('customer', models.CharField(blank=True, db_column='Customer', max_length=255, null=True)),
                ('documentid', models.OneToOneField(db_column='DocumentID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.Document')),
                ('cusaddress', models.CharField(blank=True, db_column='CusAddress', max_length=255, null=True)),
                ('payment', models.CharField(blank=True, db_column='PaymentMethod', max_length=255, null=True)),
                ('cusphone', models.CharField(blank=True, db_column='CusPhone', max_length=255, null=True)),
                ('branchid', models.ForeignKey(db_column='BranchID', on_delete=django.db.models.deletion.CASCADE, to='api.Branch')),
                ('taxid', models.ForeignKey(db_column='TaxID', on_delete=django.db.models.deletion.CASCADE, to='api.Tax')),
            ],
            options={
                'db_table': 'sell_bill',
            },
        ),
        migrations.CreateModel(
            name='Investmentrec',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, db_column='Type', max_length=255, null=True)),
                ('time', models.DateField(blank=True, db_column='Time', null=True)),
                ('desc', models.CharField(blank=True, db_column='Desc', max_length=255, null=True)),
                ('amount', models.FloatField(db_column='Amount')),
                ('income', models.FloatField(blank=True, db_column='Income', null=True)),
                ('chiefmanageruserid', models.ForeignKey(db_column='ChiefManagerUserID', on_delete=django.db.models.deletion.CASCADE, to='api.Chiefmanager')),
            ],
            options={
                'db_table': 'investmentrec',
            },
        ),
        migrations.AddField(
            model_name='document',
            name='accountantuserid',
            field=models.ForeignKey(db_column='AccountantUserID', on_delete=django.db.models.deletion.CASCADE, to='api.Accountant'),
        ),
        migrations.CreateModel(
            name='Balancerec',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('content', models.CharField(blank=True, db_column='Content', max_length=255, null=True)),
                ('amount', models.FloatField(db_column='Amount')),
                ('term', models.IntegerField(db_column='Term')),
                ('accountantuserid', models.ForeignKey(db_column='AccountantUserID', on_delete=django.db.models.deletion.CASCADE, to='api.Accountant')),
            ],
            options={
                'db_table': 'balancerec',
            },
        ),
        migrations.CreateModel(
            name='ProductSellBill',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('numinbill', models.IntegerField(blank=True, db_column='NumberInBill', null=True)),
                ('productid', models.ForeignKey(db_column='ProductID', on_delete=django.db.models.deletion.CASCADE, to='api.Product')),
                ('sellbilldocumentid', models.ForeignKey(db_column='SellBillDocumentID', on_delete=django.db.models.deletion.CASCADE, to='api.SellBill')),
            ],
            options={
                'db_table': 'product_sell_bill',
                'unique_together': {('productid', 'sellbilldocumentid')},
            },
        ),
        migrations.CreateModel(
            name='ProductBuyBill',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('numinbill', models.IntegerField(blank=True, db_column='NumberInBill', null=True)),
                ('productid', models.ForeignKey(db_column='ProductID', on_delete=django.db.models.deletion.CASCADE, to='api.Product')),
                ('buybilldocumentid', models.ForeignKey(db_column='BuyBillDocumentID', on_delete=django.db.models.deletion.CASCADE, to='api.BuyBill')),
            ],
            options={
                'db_table': 'product_buy_bill',
                'unique_together': {('productid', 'buybilldocumentid')},
            },
        ),
    ]
