"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # partner
    path('add_partner', AddPartner.as_view(), name = "add_partner"),
    path('edit_partner_info', EditPartnerInfo.as_view(), name = "edit_partner_info"),
    path('delete_partner', DeletePartner.as_view(), name = "delete_partner"),
    path('getpartners', ListPartner.as_view(), name = "getpartners"),

    # Account
    path('signin', SigninViews.as_view(), name = "signin"),
    path('create_acc', CreateAccount.as_view(), name = "create_acc"),
    path('getusers', ListUsers.as_view(), name = "listuser"),
    path('edit', EditInfo.as_view(), name = "editinfo"),
    path('delete_acc', DeleteAcc.as_view(), name = "delete_acc"),

    # product
    path('add_product', AddProduct.as_view(), name = "add_product"),
    path('edit_product_info', EditProductInfo.as_view(), name = "edit_product_info"),
    path('delete_product', DeleteProduct.as_view(), name = "delete_product"),
    path('getproducts', ListProduct.as_view(), name = "getproducts"),
    path('getproductsbypartner', GetProductByPartner.as_view(), name = "getproductsbypartner"),

    # branch
    path('get_branch', GetListBranch.as_view(), name = "get_branch"),
    path('add_branch', AddBranch.as_view(), name = "add_branch"),
    path('delete_branch', DeleteBranch.as_view(), name = "delete_branch"),
    path('edit_branch', EditInfoBranch.as_view(), name = "edit_branch"),

    # department
    path('add_department', AddDepartment.as_view(), name = "add_department"),
    path('get_department', GetDepartment.as_view(), name = "get_department"),
    path('edit_department', EditInfoDepartment.as_view(), name = "edit_department"),
    path('delete_department', DeleteDepartment.as_view(), name = "delete_department"),

    # buy Bill
    path('addbuybill', AddBuyBill.as_view(), name = "add_buy_bill"),
    path('getbuybill', GetBuyBill.as_view(), name = "get_buy_bill"),
    path('deletedocument', DeleteDocument.as_view(), name = "delete_document"),

    # sell bill
    path('addsellbill', AddSellBill.as_view(), name = "add_sell_bill"),
    path('getsellbill', GetSellBill.as_view(), name = "get_sell_bill"),

    # receipt
    path('add_receipt', AddReceipt.as_view(), name = "add_receipt"),
    path('get_receipt', GetReceipt.as_view(), name = "get_receipt"),
    path('summary_receipt', SummaryReceipt.as_view(), name = "summary_receipt"),

    # lend loan
    path('addlend', AddLend.as_view(), name = "addlend"),
    path('getlend', GetLend.as_view(), name = "getlend"),
    path('editlend', EditLend.as_view(), name = "editlend"),
    path('addloan', AddLoan.as_view(), name = "addloan"),
    path('getloan', GetLoan.as_view(), name = "getloan"),
    path('editloan', EditLoan.as_view(), name = "editloan"),
    path('addlendpaying', AddLendPaying.as_view(), name = "addlendpaying"),
    path('getlendpaying', GetLendPaying.as_view(), name = "getlendpaying"),
    path('addloanpaying', AddLoanPaying.as_view(), name = "addloanpaying"),
    path('getloanpaying', GetLoanPaying.as_view(), name = "getloanpaying"),


    path('add_employee', AddEmployee.as_view(), name = "add_employee"),
    path('get_employee', GetEmployee.as_view(), name = "get_employee"),
    path('delete_employee', DeleteEmployee.as_view(), name = "delete_employee"),
    path('edit_employee', EditInfoEmployee.as_view(), name = "edit_employee"),
    path('add_salary', AddSalary.as_view(), name = "add_salary"),
    path('get_salary', GetSalary.as_view(), name = "get_salary"),
    path('get_salary_by_employee', GetSalaryByEmployee.as_view(), name = "get_salary_by_employee"),
    path('add_tax', AddTax.as_view(), name = "add_tax"),
    path('get_salary_table', GetSalaryTable.as_view(), name = "get_salary_table"),
    path('edit_salary', EditSalary.as_view(), name = "edit_salary"),
    path('delete_salary', DeleteSalary.as_view(), name = "delete_salary"),
    path('delete_tax', DeleteTax.as_view(), name = "delete_tax"),
    path('edit_tax', EditTax.as_view(), name = "edit_tax"),
    path('get_tax', GetTax.as_view(), name = "get_tax"),
    path('add_log', AddLog.as_view(), name = "add_log"),
    path('get_log', GetLog.as_view(), name = "get_log"),
    path('edit_log', EditLog.as_view(), name = "edit_log"),
    path('delete_log', DeleteLog.as_view(), name = "delete_log"),
    path('summary_salary', SummarySalaryTable.as_view(), name = "summary_salary"),
    path('summary_buy_product', SummaryBuyProduct.as_view(), name = "summary_buy_product"),
    path('summary_sell_product', SummarySellProduct.as_view(), name = "summary_sell_product"),
    # statistic
    path('taxstatisticbybranch', TaxStatisticByBranch.as_view(), name = "taxstatisticbybranch"),
    path('salarystatisticbybranch', SalaryStatisticByBranch.as_view(), name = "salarystatisticbybranch"),
]
