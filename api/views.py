from rest_framework.views import APIView
from rest_framework.response import Response
import random
from .models import *
from .helpers.common import *
from datetime import datetime
import numpy as np

def randomDigits(digits, index):
    lower = 10**(digits-1)
    return lower + index

class ListUsers(APIView):
    def get(self, request, format=None):
        data = request.data
        users = [user for user in User.objects.all()]
        return_data = []
        if "id" in data.keys():
            userid = data['id']
        else:
            userid = None
        for user in users:
            tmp = {}
            tmp["user_id"] = user.id
            tmp["username"] = user.username
            tmp["password"] = user.password
            tmp["email"] = user.email
            tmp["address"] = user.address
            tmp["sex"] = user.sex
            if userid == user.id:
                return_data = tmp
                break
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
            id = randomDigits(8, len(users))
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
            cm = Chiefmanager(userid = user)
            cm.save()
        elif data['role'] == "Accountant":
            branch = Branch.objects.get(id=data['branch_id'])
            a = Accountant(created = datetime.now(), team = data['team'], userid = user, branchid = branch)
            a.save()
        
        return json_format(code = 200, message = "Success")

class SigninViews(APIView):
    
    def post(self, request, format=None):
        users = [user for user in User.objects.all()]
        type_acc = np.array(["Manager", "Chiefmanager", "Accountant"])
        data = request.data
        for user in users:
            
            if user.username == data["username"] and user.password == data["password"]:
                list1 = np.array([Manager.objects.filter(userid=user.id).count(), Chiefmanager.objects.filter(userid=user.id).count(), \
                    Accountant.objects.filter(userid=user.id).count()])
                data = {"id": user.id,
                        "account_type" : type_acc[list1 != 0][0]}
                return json_format(code = 200, message = "Login successfully", data = data)
        
        return json_format(code = 400, message = "Wrong username or password")

class EditInfo(APIView):
    def post(self, request, format = None):
        data = request.data
        user  = User.objects.get(id=data['id'])
        
        user.username = data["username"]
        # user.password = data["password"]
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

        partnernames = [partner.name for partner in partners]
        partnerids = [partner.id for partner in partners]
        data = request.data
        
        if data["partnername"] in partnernames:
            return json_format(code = 400, message = "Partner exist")

        partner = Partner()
        while True:
            id = randomDigits(8, len(partners))
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
        data = request.data
        if "id" in data.keys():
           partnerid = data['id']
        else:
           partnerid = None
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
        data = request.data
        branchs = [{'branch_id': branch.id,
                    'branch_name': branch.name,
                    'branch_location': branch.location} for branch in Branch.objects.all()]
        if "id" in data.keys():
            branchs = Branch.objects.get(id = data['id'])
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
            id = randomDigits(8, len(branchs))
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
        
        branch.phone = data["branch_phone"]
        branch.location = data["branch_location"]
        branch.save()

        return json_format(code = 200, message = "Success")

class AddProduct(APIView):
    def post(self, request, format = None):
        products = [product for product in Product.objects.all()]

        productnames = [product.name for product in products]
        productids = [product.id for product in products]
        data = request.data
        
        if data["name"] in productnames:
            return json_format(code = 400, message = "Product exist")

        product = Product()
        while True:
            id = randomDigits(8, len(products))
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
        product.price = data['price']
        product.numinbranch = data['numinbranch']
        product.save()

        return json_format(code = 200, message = "Success")

class ListProduct(APIView):
    def get(self, request, format=None):
        products = [product for product in Product.objects.all()]
        return_data = []
        data = request.data
        if "id" in data.keys():
            productid = data['id']
        else:
            productid = None
        for product in products:
            tmp = {}
            tmp['product_id'] = product.id
            tmp['partner_id'] = product.partnerid.id
            tmp['branch_id'] = product.branchid.id
            tmp['name'] = product.name
            tmp['price'] = product.price
            tmp['numinbranch'] = product.numinbranch
            if productid == product.id:
                return_data = tmp
                break
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
        product.price = data['price']
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
            id = randomDigits(8, len(departments))
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

class AddBill(APIView):
    def post(self, request, format = None):
        data = request.data
        user = Accountant.objects.get(userid=data['userid'])
        list_product = data['list_product']
        number_product = data['number_product']
        products = []
        sum = 0
        for productid, num in zip(list_product, number_product):
            product = Product.objects.get(id=productid)
            products.append(product)
            sum += (product.price * num)
        
        doc = Document()
        doc.accountantuserid = user
        doc.id = randomDigits(8, len(Document.objects.all()))
        doc.type = "bill"
        doc.time = datetime.now()
        doc.name = data["name"]
        doc.content = data['content']
        doc.amount = sum
        doc.save()

        bill = Bill()
        bill.billtype = data['type']
        bill.tax = data['tax']
        bill.documentid = doc
        bill.partnerid = Partner.objects.get(id = data['partnerid'])
        bill.save()

        for product, num in zip(products, number_product):
            productbill = ProductBill(productid = product, billdocumentid = bill, numinbill = num)
            productbill.save()
        
        return json_format(code = 200, message = "Success")

class GetBill(APIView):
    def get(self, request, format = None):
        res = []
        data = request.data
        for doc in Document.objects.all():
            id = doc.id
            bill = Bill.objects.get(documentid__id=id)
            product_bills = ProductBill.objects.filter(billdocumentid = id)
            res_data = {
                "billtype": bill.billtype,
                "tax": bill.tax,
                "amount": bill.documentid.amount,
                "partnerid": bill.partnerid.id,
            }
            for product_bill in product_bills:
                product = product_bill.productid
                num = product_bill.numinbill
                if "list_product" not in res_data.keys():
                    res_data["list_product"] = [product.id]
                    res_data["number_product"] = [num]
                else:
                    res_data["list_product"].append(product.id)
                    res_data["number_product"].append(num)
            if "id" in data.keys() and id == data['id']:
                res = res_data
                break
            res.append(res_data)
        return json_format(code = 200, message = "Success", data = res)

class DeleteBill(APIView):
    def post(self, request, format = None):
        data = request.data

class AddLend(APIView):
    def post(self, request, format = None):
        data = request.data
        lendrecs = [lendrec for lendrec in Lendrec.objects.all()]

        lendrec = Lendrec()
        lendrec.id = randomDigits(8, len(lendrecs))
        lendrec.partnerid = Partner.objects.get(id = data['partnerid'])
        lendrec.chiefmanageruserid = Chiefmanager.objects.get(userid__id = data['userid'])
        lendrec.desc = data['desc']
        lendrec.amount = data['amount']
        lendrec.time = datetime.now()
        lendrec.interest_rate = data['interest_rate']
        lendrec.save()
        return json_format(code = 200, message = "Success")

class GetLend(APIView):
    def get(self, request, format = None):
        data = request.data
        lendrecs = [lendrec for lendrec in Lendrec.objects.all()]
        redata = []
        for lendrec in lendrecs:
            tmp = dict()
            tmp['id'] = lendrec.id
            tmp["partnerid"] = lendrec.partnerid.id
            tmp['userid'] = lendrec.chiefmanageruserid.userid.id
            tmp['desc'] = lendrec.desc
            tmp['amount'] = lendrec.amount
            tmp['time'] = lendrec.time
            tmp['interest_rate'] = lendrec.interest_rate

            if "id" in data.keys() and data['id'] == lendrec.id:
                redata = tmp
                break
            redata.append(tmp)
        return json_format(code = 200, message = "Success", data = redata)

class EditLend(APIView):
    def post(self, request, format = None):
        data = request.data
