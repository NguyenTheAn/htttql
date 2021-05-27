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
            a = Accountant(created = datetime.now(), userid = user, branchid = branch)
            a.save()
        
        return json_format(code = 200, message = "Success")

class SigninViews(APIView):
    
    def post(self, request, format=None):
        users = [user for user in User.objects.all()]
        type_acc = np.array(["Manager", "Chiefmanager", "Accountant"])
        instance = np.array([Manager, Chiefmanager, Accountant])
        data = request.data
        for user in users:
            
            if user.username == data["username"] and user.password == data["password"]:
                list1 = np.array([Manager.objects.filter(userid=user.id).count(), Chiefmanager.objects.filter(userid=user.id).count(), \
                    Accountant.objects.filter(userid=user.id).count()])
                account_type = type_acc[list1 != 0][0]
                data = {"id": user.id,
                        "account_type" : account_type}
                if account_type != "Chiefmanager":
                    data["branchid"] = instance[list1 != 0][0].objects.get(userid__id = user.id).branchid.id

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
                    'branch_phone': branch.phone,
                    'branch_location': branch.location} for branch in Branch.objects.all()]
        if "id" in data.keys():
            branchs = Branch.objects.get(id = data['id'])
        return json_format(code = 200, message = "Success", data = branchs)

class AddBranch(APIView):
    def post(self, request, format=None):
        branchs = [branch for branch in Branch.objects.all()]
        data = request.data

        branch = Branch()
        branch.id = randomDigits(8, len(branchs))
        branch.phone = data['branch_phone']
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
        data = request.data
        
        if data["name"] in productnames:
            return json_format(code = 400, message = "Product exist")

        product = Product()
        product.id = randomDigits(8, len(products))
        
        branch_id = data['branch_id']
        branch = Branch.objects.get(id=branch_id)
        partner_id = data['partner_id']
        partner = Partner.objects.get(id=partner_id)

        product.partnerid = partner
        product.branchid = branch
        product.name = data['name']
        product.ctrprice = data['ctrprice']
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
            tmp['ctrprice'] = product.ctrprice
            tmp['inprice'] = product.inprice
            tmp['outprice'] = product.outprice
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

        if "branch_id" in data.keys():
            branch_id = data['branch_id']
            branch = Branch.objects.get(id=branch_id)
            product.branchid = branch
        if "partner_id" in data.keys():
            partner_id = data['partner_id']
            partner = Partner.objects.get(id=partner_id)
            product.partnerid = partner
        if "name" in data.keys():
            product.name = data['name']
        if "numinbranch" in data.keys():
            product.numinbranch = data['numinbranch']
        if "ctrprice" in data.keys():
            product.ctrprice = data['ctrprice']
        if "inprice" in data.keys():
            product.inprice = data['inprice']
        if "outprice" in data.keys():
            product.outprice = data['outprice']
        product.save()

        return json_format(code = 200, message = "Success")

class DeleteProduct(APIView):
    def post(self, request, format=None):
        data = request.data
        product = Product.objects.get(id=data["id"])
        product.delete()
        return json_format(code = 200, message = "Success")

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

class AddBuyBill(APIView):
    def post(self, request, format = None):
        data = request.data
        user = Accountant.objects.get(userid=data['userid'])
        branch = Branch.objects.get(id = data['branchid'])

        list_product = data['list_product']
        number_product = data['number_product']
        products = [Product.objects.get(id = productid) for productid in list_product]
        
        doc = Document()
        doc.accountantuserid = user
        doc.id = randomDigits(8, len(Document.objects.all()))
        doc.type = "bill"
        doc.time = datetime.now()
        doc.name = data["name"]
        doc.content = data['content']
        doc.amount = data['amount']
        doc.save()

        bill = BuyBill()
        bill.branchid = branch
        bill.documentid = doc
        bill.payment = data['payment']
        bill.save()

        for product, num in zip(products, number_product):
            product.inprice = data['amount']
            product.numinbranch += num
            product.save()
            id = randomDigits(8, len(ProductBuyBill.objects.all()))
            productbill = ProductBuyBill(id = id, productid = product, buybilldocumentid = bill, numinbill = num)
            productbill.save()
        
        return json_format(code = 200, message = "Success")

class GetBuyBill(APIView):
    def get(self, request, format = None):
        res = []
        data = request.data
        for doc in Document.objects.all():
            id = doc.id
            bill = BuyBill.objects.get(documentid__id=id)
            product_bills = ProductBuyBill.objects.filter(buybilldocumentid__documentid__id = id)
            res_data = {
                "documentid": bill.documentid.id,
                "payment": bill.payment,
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

class DeleteDocument(APIView):
    def post(self, request, format = None):
        data = request.data
        doc = Document.objects.get(id = data['id'])
        doc.delete()
        return json_format(code = 200, message = "Success")

class AddSellBill(APIView):
    def post(self, request, format = None):
        data = request.data
        user = Accountant.objects.get(userid=data['userid'])
        branch = Branch.objects.get(id = data['branchid'])

        list_product = data['list_product']
        number_product = data['number_product']
        products = [Product.objects.get(id = productid) for productid in list_product]
        
        doc = Document()
        doc.accountantuserid = user
        doc.id = randomDigits(8, len(Document.objects.all()))
        doc.type = "bill"
        doc.time = datetime.now()
        doc.name = data["name"]
        doc.content = data['content']
        doc.save()

        bill = SellBill()
        bill.branchid = branch
        bill.documentid = doc
        bill.customer = data['customer']
        bill.cusaddress = data['cusaddress']
        bill.customer = data['customer']
        bill.cusphone = data['cusphone']
        tax = Tax.objects.get(id = data['taxid'])
        bill.taxid = tax
        bill.save()

        for product, num in zip(products, number_product):
            product.numinbranch -= num
            product.save()
            id = randomDigits(8, len(ProductSellBill.objects.all()))
            productbill = ProductSellBill(id = id, productid = product, sellbilldocumentid = bill, numinbill = num)
            productbill.save()
        
        return json_format(code = 200, message = "Success")

class GetSellBill(APIView):
    def get(self, request, format = None):
        res = []
        data = request.data
        for doc in Document.objects.all():
            id = doc.id
            bill = SellBill.objects.get(documentid__id=id)
            product_bills = ProductSellBill.objects.filter(sellbilldocumentid__documentid__id = id)
            res_data = {
                "documentid": bill.documentid.id,
                "customer": bill.customer,
                "cusaddress": bill.cusaddress,
                "cusphone": bill.cusphone,
                "payment": bill.payment,
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
        lendrec.time = datetime.strptime(data['time'], "%d/%m/%Y")
        lendrec.expired = datetime.strptime(data['expired'], "%d/%m/%Y")
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
            tmp['time'] = lendrec.time.strftime("%d/%m/%Y")
            tmp['expired'] = lendrec.expired.strftime("%d/%m/%Y")
            tmp['interest_rate'] = lendrec.interest_rate

            if "id" in data.keys() and data['id'] == lendrec.id:
                redata = tmp
                break
            redata.append(tmp)
        return json_format(code = 200, message = "Success", data = redata)

class EditLend(APIView):
    def post(self, request, format = None):
        data = request.data
        lendrec = Lendrec.objects.get(id = data['id'])

        lendrec.desc = data['desc'] 
        lendrec.amount = data['amount'] 
        lendrec.time = datetime.strptime(data['time'], "%d/%m/%Y")
        lendrec.expired = datetime.strptime(data['expired'], "%d/%m/%Y")
        lendrec.interest_rate = data['interest_rate'] 
        lendrec.save()

        return json_format(code = 200, message = "Success")

class AddLoan(APIView):
    def post(self, request, format = None):
        data = request.data
        loanrecs = [loanrec for loanrec in Loanrec.objects.all()]

        loanrec = Loanrec()
        loanrec.id = randomDigits(8, len(loanrecs))
        loanrec.chiefmanageruserid = Chiefmanager.objects.get(userid__id = data['userid'])
        loanrec.desc = data['desc']
        loanrec.amount = data['amount']
        loanrec.time = datetime.strptime(data['time'], "%d/%m/%Y")
        loanrec.expired = datetime.strptime(data['expired'], "%d/%m/%Y")
        loanrec.interest_rate = data['interest_rate']
        loanrec.save()

        return json_format(code = 200, message = "Success")

class GetLoan(APIView):
    def get(self, request, format = None):
        data = request.data
        loanrecs = [loanrec for loanrec in Loanrec.objects.all()]
        redata = []
        for loanrec in loanrecs:
            tmp = dict()
            tmp['id'] = loanrec.id
            tmp['userid'] = loanrec.chiefmanageruserid.userid.id
            tmp['desc'] = loanrec.desc
            tmp['amount'] = loanrec.amount
            tmp['time'] = loanrec.time.strftime("%d/%m/%Y")
            tmp['expired'] = loanrec.expired.strftime("%d/%m/%Y")
            tmp['interest_rate'] = loanrec.interest_rate

            if "id" in data.keys() and data['id'] == loanrec.id:
                redata = tmp
                break
            redata.append(tmp)
        return json_format(code = 200, message = "Success", data = redata)

class EditLoan(APIView):
    def post(self, request, format = None):
        data = request.data
        loanrec = Loanrec.objects.get(id = data['id'])

        loanrec.desc = data['desc'] 
        loanrec.amount = data['amount'] 
        loanrec.time = datetime.strptime(data['time'], "%d/%m/%Y")
        loanrec.expired = datetime.strptime(data['expired'], "%d/%m/%Y")
        loanrec.interest_rate = data['interest_rate'] 
        loanrec.save()

        return json_format(code = 200, message = "Success")

class AddInvestment(APIView):
    def post(self, request, format = None):
        data = request.data
        investmentrecs = [investmentrec for investmentrec in Investmentrec.objects.all()]

        investmentrec = Loanrec()
        investmentrec.id = randomDigits(8, len(investmentrecs))
        investmentrec.chiefmanageruserid = Chiefmanager.objects.get(userid__id = data['userid'])
        investmentrec.desc = data['desc']
        investmentrec.amount = data['amount']
        investmentrec.time = datetime.strptime(data['time'], "%d/%m/%Y")
        investmentrec.type = data['type']
        investmentrec.save()

        return json_format(code = 200, message = "Success")

class GetInvestment(APIView):
    def get(self, request, format = None):
        data = request.data
        investmentrecs = [investmentrec for investmentrec in Investmentrec.objects.all()]
        redata = []
        for investmentrec in investmentrecs:
            tmp = dict()
            tmp['id'] = investmentrec.id
            tmp['userid'] = investmentrec.chiefmanageruserid.userid.id
            tmp['desc'] = investmentrec.desc
            tmp['amount'] = investmentrec.amount
            tmp['time'] = investmentrec.time.strftime("%d/%m/%Y")
            tmp['type'] = investmentrec.type

            if "id" in data.keys() and data['id'] == investmentrec.id:
                redata = tmp
                break
            redata.append(tmp)
        return json_format(code = 200, message = "Success", data = redata)

class EditInvestment(APIView):
    def post(self, request, format = None):
        data = request.data
        investmentrec = Investmentrec.objects.get(id = data['id'])

        investmentrec.desc = data['desc'] 
        investmentrec.amount = data['amount'] 
        investmentrec.time = datetime.strptime(data['time'], "%d/%m/%Y")
        investmentrec.type = data['interest_rate'] 
        investmentrec.save()

        return json_format(code = 200, message = "Success")

class AddReport(APIView):
    def post(self, request, format = None):
        data = request.data