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
    path('create_acc', CreateAccount.as_view(), name = "create_acc"),
    path('delete_acc', DeleteAcc.as_view(), name = "delete_acc"),
    path('signin', SigninViews.as_view(), name = "signin"),
    path('users', ListUsers.as_view(), name = "listuser"),
    path('edit', EditInfo.as_view(), name = "editinfo"),
    path('get_branch', GetListBranch.as_view(), name = "get_branch"),
    path('add_branch', AddBranch.as_view(), name = "add_branch"),
    path('delete_branch', DeleteBranch.as_view(), name = "delete_branch"),
    path('edit_branch', EditInfoBranch.as_view(), name = "edit_branch"),
    path('add_department', AddDepartment.as_view(), name = "add_department"),
    path('get_department', GetDepartment.as_view(), name = "get_department"),
    path('edit_department', EditInfoDepartment.as_view(), name = "edit_department"),
    path('delete_department', DeleteDepartment.as_view(), name = "delete_department"),
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
]
