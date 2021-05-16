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
]
