from rest_framework.views import APIView
from rest_framework.response import Response
import random
from .models import *
from .helpers.common import *
from datetime import datetime

def randomDigits(digits):
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)

class ListUsers(APIView):
    def get(self, request, format=None):
        users = [user for user in User.objects.all()]
        return_data = []
        for user in users:
            tmp = {}
            tmp["user_id"] = user.id
            tmp["username"] = user.username
            tmp["password"] = user.password
            tmp["email"] = user.email
            tmp["address"] = user.address
            tmp["sex"] = user.sex
            return_data.append(tmp)

        return json_format(code = 200, message = "Success", data = return_data)

class CreateAccount(APIView):
    
    def post(self, request, format=None):
        users = [user for user in User.objects.all()]
        usernames = [user.username for user in users]
        userids = [user.id for user in users]
        data = request.data
        
        if data["username"] in usernames:
            return json_format(code = 400, message = "Account exist")

        user = User()
        while True:
            id = randomDigits(8)
            if id not in userids:
                user.id = id
                break
        user.username = data["username"]
        user.password = data["password"]
        user.email = data["email"]
        user.phone = data['phone']
        user.sex = data['sex']
        user.address = data["address"]
        user.save()

        if data['role'] == "Manager":
            branch = Branch.objects.get(id=data['branch_id'])
            m = Manager(userid = user, created = datetime.now(), branchid = branch)
            m.save()
        elif data['role'] == "Chiefmanager":
            cm = Chiefmanager(userid = user, cardid = data['card_id'])
            cm.save()
        elif data['role'] == "Accountant":
            branch = Branch.objects.get(id=data['branch_id'])
            a = Accountant(created = datetime.now(), team = data['team'], userid = user, branchid = branch)
            a.save()
        
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

class DeleteAcc(APIView):
    def post(self, request, format = None):
        data = request.data
        id = data['user_id']
        user = User.objects.get(id=id)
        user.delete()
        return json_format(code = 200, message = "Success")

class AddPartner(APIView):
    def post(self, request, format = None):
        partners = [partner for partner in Partner.objects.all()]

        partnernames = [partner.username for partner in partners]
        partnerids = [partner.id for partner in partners]
        data = request.data
        
        if data["partnername"] in partnernames:
            return json_format(code = 400, message = "Partner exist")

        partner = Partner()
        while True:
            id = randomDigits(8)
            if id not in partnerids:
                partner.id = id
                break
        
        partner.name = data["partnername"]
        partner.taxid = data["taxid"]
        partner.address = data['address']
        partner.desc = data["desc"]
        partner.phone = data["phone"]
        partner.email = data["email"]
        partner.save()

        return json_format(code = 200, message = "Success")

class ListPartner(APIView):
    def get(self, request, format=None):
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
            return_data.append(tmp)

        return json_format(code = 200, message = "Success", data = return_data)

class EditPartnerInfo(APIView):
    def post(self, request, format = None):
        data = request.data
        partner  = Partner.objects.get(id=data['id'])
        
        partner.name = data["partnername"]
        partner.taxid = data["taxid"]
        partner.email = data["email"]
        partner.phone = data['phone']
        partner.desc = data['desc']
        partner.address = data["address"]
        partner.save()

        return json_format(code = 200, message = "Success")

class DeletePartner(APIView):
    def post(self, request, format = None):
        data = request.data
        id = data['partner_id']
        partner = Partner.objects.get(id=id)
        partner.delete()
        return json_format(code = 200, message = "Success")

class GetListBranch(APIView):
    def get(self, request, format=None):
        branchs = [{'branch_id': branch.id,
                    'branch_name': branch.name,
                    'branch_location': branch.location} for branch in Branch.objects.all()]
        return json_format(code = 200, message = "Success", data = branchs)

class AddBranch(APIView):
    def post(self, request, format=None):
        branchs = [branch for branch in Branch.objects.all()]
        branch_name = [branch.name for branch in branchs]
        branch_id = [branch.id for branch in branchs]
        data = request.data
        
        if data["branch_name"] in branch_name:
            return json_format(code = 400, message = "Branch exist")

        branch = Branch()
        while True:
            id = randomDigits(8)
            if id not in branch_id:
                branch.id = id
                break
        branch.name = data['branch_name']
        branch.location = data['branch_location']
        branch.save()

        return json_format(code = 200, message = "Success")

class DeleteBranch(APIView):
    def post(self, request, format=None):
        data = request.data
        branch = Branch.objects.get(id=data["branch_id"])
        branch.delete()
        return json_format(code = 200, message = "Success")

class EditInfoBranch(APIView):
    def post(self, request, format = None):
        data = request.data
        branch  = Branch.objects.get(id=data['branch_id'])
        
        branch.name = data["branch_name"]
        branch.location = data["branch_location"]
        branch.save()

        return json_format(code = 200, message = "Success")

class AddProduct(APIView):
    def post(self, request, format = None):
        products = [product for product in Product.objects.all()]

        productnames = [product.username for product in products]
        productids = [product.id for product in products]
        data = request.data
        
        if data["name"] in productnames:
            return json_format(code = 400, message = "Product exist")

        product = Product()
        while True:
            id = randomDigits(8)
            if id not in productids:
                product.id = id
                break
        
        branch_id = data['branch_id']
        branch = Branch.objects.get(id=branch_id)
        partner_id = data['partner_id']
        partner = Partner.objects.get(id=partner_id)

        product.partnerid = partner
        product.branchid = branch
        product.name = data['name']
        product.type = data['type']
        product.price = data['price']
        product.category = data['category']
        product.numinbranch = data['numinbranch']
        product.save()

        return json_format(code = 200, message = "Success")

class ListProduct(APIView):
    def get(self, request, format=None):
        products = [product for product in Product.objects.all()]
        return_data = []
        for product in products:
            tmp = {}
            tmp['product_id'] = product.id
            tmp['partner_id'] = product.partnerid.id
            tmp['branch_id'] = product.branchid.id
            tmp['name'] = product.name
            tmp['type'] = product.type
            tmp['price'] = product.price
            tmp['category'] = product.category
            tmp['numinbranch'] = product.numinbranch
            return_data.append(tmp)

        return json_format(code = 200, message = "Success", data = return_data)

class EditProductInfo(APIView):
    def post(self, request, format = None):
        data = request.data
        product  = Product.objects.get(id=data['id'])

        branch_id = data['branch_id']
        branch = Branch.objects.get(id=branch_id)
        partner_id = data['partner_id']
        partner = Partner.objects.get(id=partner_id)
        
        product.partnerid = partner
        product.branchid = branch
        product.name = data['name']
        product.type = data['type']
        product.price = data['price']
        product.category = data['category']
        product.numinbranch = data['numinbranch']
        product.save()

        return json_format(code = 200, message = "Success")

class DeleteProduct(APIView):
    def post(self, request, format=None):
        data = request.data
        product = Product.objects.get(id=data["id"])
        product.delete()
class GetDepartment(APIView):
    def get(self, request, format=None):
        departments = [{'department_id': department.id,
                        'branch_id': department.branchid.id,
                        'department_name': department.name,
                        'department_numofemployees': department.numofemployees} for department in Department.objects.all()]

        return json_format(code = 200, message = "Success", data = departments)

class AddDepartment(APIView):
    def post(self, request, format=None):
        departments = [department for department in Department.objects.all()]
        department_name = [department.name for department in departments]
        department_id = [department.id for department in departments]
        data = request.data
        
        if data["department_name"] in department_name:
            return json_format(code = 400, message = "Department exist")

        department = Department()
        while True:
            id = randomDigits(8)
            if id not in department_id:
                department.id = id
                break
        department.name = data['department_name']
        branch = Branch.objects.get(id=data['branch_id'])
        department.branchid = branch
        department.numofemployees = 0
        department.save()

        return json_format(code = 200, message = "Success")

class EditInfoDepartment(APIView):
    def post(self, request, format = None):
        data = request.data
        department  = Department.objects.get(id=data['department_id'])
        
        department.name = data["department_name"]
        branch = Branch.objects.get(id=data['branch_id'])
        department.brandid = branch
        department.save()

        return json_format(code = 200, message = "Success")

class DeleteDepartment(APIView):
    def post(self, request, format=None):
        data = request.data
        department = Department.objects.get(id=data["department_id"])
        department.delete()
        return json_format(code = 200, message = "Success")