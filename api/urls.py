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
]
