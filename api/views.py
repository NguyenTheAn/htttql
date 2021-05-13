from rest_framework.views import APIView
from rest_framework.response import Response
import random
from .models import *
from .helpers.common import *

def randomDigits(digits):
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)

class ListUsers(APIView):
    def get(self, request, format=None):
        usernames = [user.userID for user in User.objects.all()]
        return json_format(code = 200, message = "Success", data = usernames)

class SignupViews(APIView):
    
    def post(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        data = request.data
        if data["username"] in usernames:
            return json_format(code = 400, message = "Account exist")

        user = User()
        user.id = randomDigits(8)
        user.username = data["username"]
        user.password = data["password"]
        user.email = data["email"]
        user.phone = data['phone']
        user.sex = data['sex']
        user.address = data["address"]
        user.save()
        
        return json_format(code = 200, message = "Success")

class SigninViews(APIView):
    
    def post(self, request, format=None):
        users = [user for user in User.objects.all()]
        data = request.data
        for user in users:
            if user.username == data["username"] and user.password == data["password"]:
                return json_format(code = 200, message = "Login successfully")
        
        return json_format(code = 400, message = "Wrong username or password")

class EditInfo(APIView):
    def post(self, request, format = None):
        data = request.data
        user  = User.objects.get(id=data['id'])
        
        user.username = data["username"]
        user.password = data["password"]
        user.email = data["email"]
        user.phone = data['phone']
        user.sex = data['sex']
        user.address = data["address"]
        user.save()

        return json_format(code = 200, message = "Success")