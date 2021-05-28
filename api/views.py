from rest_framework.views import APIView
from rest_framework.response import Response
import random
from .models import *
from .helpers.common import *
import datetime
import numpy as np
from calendar import monthrange
from .helpers.helpers import *

def randomDigits(digits, index):
    lower = 10**(digits-1)
    return lower + index

class ListUsers(APIView):
    def get(self, request, format=None):
        data = request.data
        if "id" in data.keys():
            userid = data['id']
        else:
            userid = None
        return_data = getUser(userid)

        return json_format(code = 200, message = "Success", data = return_data)

class CreateAccount(APIView):
    
    def post(self, request, format=None):
        users = [user for user in User.objects.all()]
        usernames = [user.username for user in users]
        data = request.data
        
        if data["username"] in usernames:
            return json_format(code = 400, message = "Account exist")

        user = User()
        userids = [int(user.id) for user in users]
        if len(userids) != 0:
            index = max(userids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)

        user.id = id
        user.username = data["username"]
        user.password = data["password"]
        user.email = data["email"]
        user.phone = data['phone']
        user.sex = data['sex']
        user.address = data["address"]
        user.save()

        if data['role'] == "Admin":
            a = Admin(userid = user)
            a.save()
        elif data['role'] == "Manager":
            branch = Branch.objects.get(id=data['branch_id'])
            m = Manager(userid = user, created = datetime.datetime.now(), branchid = branch)
            m.save()
        elif data['role'] == "Chiefmanager":
            cm = Chiefmanager(userid = user)
            cm.save()
        elif data['role'] == "Accountant":
            branch = Branch.objects.get(id=data['branch_id'])
            a = Accountant(created = datetime.datetime.now(), userid = user, branchid = branch)
            a.save()
        
        return json_format(code = 200, message = "Success")

class SigninViews(APIView):
    
    def post(self, request, format=None):
        users = [user for user in User.objects.all()]
        data = request.data
        for user in users:
            if user.username == data["username"] and user.password == data["password"]:
                data = getUser(user.id)

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
        partnerids = [int(partner.id) for partner in partners]
        data = request.data
        
        if data["partnername"] in partnernames:
            return json_format(code = 400, message = "Partner exist")

        partner = Partner()
        if len(partnerids) != 0:
            index = max(partnerids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        
        partner.id = id
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
        return_data = []
        data = request.data
        if "id" in data.keys():
           partnerid = data['id']
        else:
           partnerid = None
        return_data = getPartner(partnerid)

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
        if "branchid" in data.keys():
           branchid = data['id']
        else:
           branchid = None
        branchs = getBranch(branchid)
        return json_format(code = 200, message = "Success", data = branchs)

class AddBranch(APIView):
    def post(self, request, format=None):
        branchs = [branch for branch in Branch.objects.all()]
        branch_phone = [branch.phone for branch in branchs]
        branch_id = [int(branch.id) for branch in branchs]
        data = request.data
        
        if data["branch_phone"] in branch_phone:
            return json_format(code = 400, message = "Branch exist")

        branch = Branch()
        if len(branch_id) != 0:
            index = max(branch_id) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        
        branch.id = id
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
        
        if "branch_phone" in data.keys():
            branch.phone = data["branch_phone"]
        if "branch_location" in data.keys():
            branch.location = data["branch_location"]
        branch.save()

        return json_format(code = 200, message = "Success")

class AddProduct(APIView):
    def post(self, request, format = None):
        products = [product for product in Product.objects.all()]
        productnames = [product.name for product in products]
        productids = [int(product.id) for product in products]
        data = request.data
        
        if data["name"] in productnames:
            return json_format(code = 400, message = "Product exist")

        product = Product()
        if len(productids) != 0:
            index = max(productids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        
        branch_id = data['branch_id']
        branch = Branch.objects.get(id=branch_id)
        partner_id = data['partner_id']
        partner = Partner.objects.get(id=partner_id)

        product.id = id
        product.partnerid = partner
        product.branchid = branch
        product.name = data['name']
        product.ctrprice = data['ctrprice']
        product.save()

        return json_format(code = 200, message = "Success")

class ListProduct(APIView):
    def get(self, request, format=None):
        return_data = []
        data = request.data
        if "id" in data.keys():
            productid = data['id']
        else:
            productid = None

        return_data = getProduct(productid)

        return json_format(code = 200, message = "Success", data = return_data)

class GetProductByPartner(APIView):
    def get(self, request, format=None):
        return_data = []
        data = request.data
        partnerid = data['partnerid']
        products = Product.objects.filter(partnerid__id = partnerid)
        for product in products:
            return_data.append(getProduct(product.id))
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
        data = request.data
        if "departmentid" in data.keys():
            departmentid = data['departmentid']
        else:
            departmentid = None
        departments = getDepartment(departmentid)

        return json_format(code = 200, message = "Success", data = departments)

class AddDepartment(APIView):
    def post(self, request, format=None):
        departments = [department for department in Department.objects.all()]
        department_name = [department.name for department in departments]
        department_id = [int(department.id) for department in departments]
        data = request.data
        
        if data["department_name"] in department_name:
            return json_format(code = 400, message = "Department exist")

        department = Department()
        if len(department_id) != 0:
            index = max(department_id) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        department.id = id
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
        
        if "department_name" in data.keys():
            department.name = data["department_name"]
        if "branch_id" in data.keys():
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
        list_price = data['list_price']
        products = [Product.objects.get(id = productid) for productid in list_product]
        
        amount = 0
        for price, num in zip(number_product, list_price):
            amount += (price*num)
        doc = Document()
        doc.accountantuserid = user
        doc.id = randomDigits(8, len(Document.objects.all()))
        doc.type = "bill"
        doc.time = datetime.datetime.now()
        doc.name = data["name"]
        doc.content = data['content']
        doc.amount = amount
        doc.save()

        bill = BuyBill()
        bill.branchid = branch
        bill.documentid = doc
        bill.payment = data['payment']
        bill.save()

        for product, num, price in zip(products, number_product, list_price):
            product.inprice = price
            product.numinbranch += num
            product.save()
            productbuybillsids = [int(pro.id) for pro in ProductBuyBill.objects.all()]
            if len(productbuybillsids) != 0:
                index = max(productbuybillsids) - 10000000 + 1
            else:
                index = 0
            id = randomDigits(8, index)
            productbill = ProductBuyBill(id = id, productid = product, buybilldocumentid = bill, numinbill = num)
            productbill.save()
        
        return json_format(code = 200, message = "Success")

class GetBuyBill(APIView):
    def get(self, request, format = None):
        res = []
        data = request.data
        for doc in Document.objects.all():
            id = doc.id
            bill = BuyBill.objects.filter(documentid__id=id)
            if bill.count() != 0:
                bill = bill[0]
            else:
                continue
            product_bills = ProductBuyBill.objects.filter(buybilldocumentid__documentid__id = id)
            res_data = {
                "documentid": bill.documentid.id,
                "payment": bill.payment,
            }
            for product_bill in product_bills:
                product = product_bill.productid
                num = product_bill.numinbill
                if "list_product" not in res_data.keys():
                    product_data = getProduct(product.id)
                    product_data["numinbill"] = num
                    res_data["list_product"] = [product_data]
                else:
                    product_data = getProduct(product.id)
                    product_data["numinbill"] = num
                    res_data["list_product"].append(product_data)
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
        list_price = data['list_price']
        products = [Product.objects.get(id = productid) for productid in list_product]

        amount = 0
        for price, num in zip(number_product, list_price):
            amount += (price*num)
        
        doc = Document()
        doc.accountantuserid = user
        doc.id = randomDigits(8, len(Document.objects.all()))
        doc.type = "bill"
        doc.time = datetime.datetime.now()
        doc.name = data["name"]
        doc.content = data['content']
        doc.amount = amount
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
            productsellbillsids = [int(pro.id) for pro in ProductSellBill.objects.all()]
            if len(productsellbillsids) != 0:
                index = max(productsellbillsids) - 10000000 + 1
            else:
                index = 0
            id = randomDigits(8, index)
            productbill = ProductSellBill(id = id, productid = product, sellbilldocumentid = bill, numinbill = num)
            productbill.save()
        
        return json_format(code = 200, message = "Success")

class GetSellBill(APIView):
    def get(self, request, format = None):
        res = []
        data = request.data
        for doc in Document.objects.all():
            id = doc.id
            bill = SellBill.objects.filter(documentid__id=id)
            if bill.count() != 0:
                bill = bill[0]
            else:
                continue
            product_bills = ProductSellBill.objects.filter(sellbilldocumentid__documentid__id = id)
            res_data = {
                "documentid": bill.documentid.id,
                "customer": bill.customer,
                "cusaddress": bill.cusaddress,
                "cusphone": bill.cusphone,
                "payment": bill.payment,
                "amount": bill.documentid.amount
            }
            for product_bill in product_bills:
                product = product_bill.productid
                num = product_bill.numinbill
                if "list_product" not in res_data.keys():
                    product_data = getProduct(product.id)
                    product_data["numinbill"] = num
                    res_data["list_product"] = [product_data]
                else:
                    product_data = getProduct(product.id)
                    product_data["numinbill"] = num
                    res_data["list_product"].append(product_data)
            if "id" in data.keys() and id == data['id']:
                res = res_data
                break
            res.append(res_data)
        return json_format(code = 200, message = "Success", data = res)

class AddLend(APIView):
    def post(self, request, format = None):
        data = request.data
        lendrecs = [lendrec for lendrec in Lendrec.objects.all()]
        lendrecids = [int(lendrec.id) for lendrec in lendrecs]

        lendrec = Lendrec()
        
        if len(lendrecids) != 0:
            index = max(lendrecids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        lendrec.id = id
        lendrec.partnerid = Partner.objects.get(id = data['partnerid'])
        lendrec.chiefmanageruserid = Chiefmanager.objects.get(userid__id = data['userid'])
        lendrec.desc = data['desc']
        lendrec.amount = data['amount']
        lendrec.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        lendrec.expired = datetime.datetime.strptime(data['expired'], "%d/%m/%Y")
        lendrec.interest_rate = data['interest_rate']
        lendrec.save()
        return json_format(code = 200, message = "Success")

class GetLend(APIView):
    def get(self, request, format = None):
        data = request.data
        if 'id' in data.keys():
            lendid = data['id']
        else:
            lendid = None
        redata = getLend(lendid)
        return json_format(code = 200, message = "Success", data = redata)

class EditLend(APIView):
    def post(self, request, format = None):
        data = request.data
        lendrec = Lendrec.objects.get(id = data['id'])

        lendrec.desc = data['desc'] 
        lendrec.amount = data['amount'] 
        lendrec.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        lendrec.expired = datetime.datetime.strptime(data['expired'], "%d/%m/%Y")
        lendrec.interest_rate = data['interest_rate'] 
        lendrec.save()

        return json_format(code = 200, message = "Success")

class AddLendPaying(APIView):
    def post(self, request, format = None):
        data = request.data
        lendpayings = [lendpaying for lendpaying in LendPaying.objects.all()]
        lendpayingids = [int(lendpaying.id) for lendpaying in lendpayings]
        lendrec = Lendrec.objects.get(id = data['lendrecid'])

        lendpaying = LendPaying()
        if len(lendpayingids) != 0:
            index = max(lendpayingids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        lendpaying.id = id
        lendpaying.lendrecid = lendrec
        lendpaying.interestamount = data['interest_amount']
        lendpaying.payingamount = data['payingamount']
        lendpaying.time = datetime.datetime.now()
        lendpaying.payment = data['payment']
        lendpaying.save()
        return json_format(code = 200, message = "Success")

class AddLoanPaying(APIView):
    def post(self, request, format = None):
        data = request.data
        loanpayings = [loanpaying for loanpaying in LoanPaying.objects.all()]
        loanpayingids = [int(loanpaying.id) for loanpaying in loanpayings]
        loanrec = Loanrec.objects.get(id = data['loanrecid'])

        loanpaying = LoanPaying()
        if len(loanpayingids) != 0:
            index = max(loanpayingids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        loanpaying.id = id
        loanpaying.loanrecid = loanrec
        loanpaying.interestamount = data['interest_amount']
        loanpaying.payingamount = data['payingamount']
        loanpaying.time = datetime.datetime.now()
        loanpaying.payment = data['payment']
        loanpaying.save()
        return json_format(code = 200, message = "Success")

class GetLendPaying(APIView):
    def get(self, request, format = None):
        data = request.data
        if "id" in data.keys():
            lenpayingid = data['id']
        else:
            lenpayingid = None
        lenpayings = getLendPaying(lenpayingid)
        return json_format(code = 200, message = "Success", data = lenpayings)

class AddLoan(APIView):
    def post(self, request, format = None):
        data = request.data
        loanrecs = [loanrec for loanrec in Loanrec.objects.all()]
        loanrecids = [int(loanrec.id) for loanrec in Loanrec.objects.all()]

        loanrec = Loanrec()
        if len(loanrecids) != 0:
            index = max(loanrecids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        loanrec.id = id
        loanrec.chiefmanageruserid = Chiefmanager.objects.get(userid__id = data['userid'])
        loanrec.desc = data['desc']
        loanrec.amount = data['amount']
        loanrec.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        loanrec.expired = datetime.datetime.strptime(data['expired'], "%d/%m/%Y")
        loanrec.interest_rate = data['interest_rate']
        loanrec.save()

        return json_format(code = 200, message = "Success")

class GetLoan(APIView):
    def get(self, request, format = None):
        data = request.data
        if 'id' in data.keys():
            loanid = data['id']
        else:
            loanid = None
        redata = getLoan(loanid)
        return json_format(code = 200, message = "Success", data = redata)

class GetLoanPaying(APIView):
    def get(self, request, format = None):
        data = request.data
        if 'id' in data.keys():
            loanpayingid = data['id']
        else:
            loanpayingid = None
        redata = getLoanPaying(loanpayingid)
        return json_format(code = 200, message = "Success", data = redata)

class EditLoan(APIView):
    def post(self, request, format = None):
        data = request.data
        loanrec = Loanrec.objects.get(id = data['id'])

        loanrec.desc = data['desc'] 
        loanrec.amount = data['amount'] 
        loanrec.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        loanrec.expired = datetime.datetime.strptime(data['expired'], "%d/%m/%Y")
        loanrec.interest_rate = data['interest_rate'] 
        loanrec.save()

        return json_format(code = 200, message = "Success")

class AddInvestment(APIView):
    def post(self, request, format = None):
        data = request.data
        investmentrecs = [investmentrec for investmentrec in Investmentrec.objects.all()]
        investmentrecids = [int(investmentrec.id) for investmentrec in investmentrecs]

        investmentrec = Loanrec()
        if len(investmentrecids) != 0:
            index = max(investmentrecids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        investmentrec.id = id
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
            tmp['userid'] = getUser(investmentrec.chiefmanageruserid.userid.id)
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

class AddTax(APIView):
    def post(self, request, format=None):
        taxes_ids = [int(tax.id) for tax in Tax.objects.all()]
        data = request.data

        tax = Tax()
        if len(taxes_ids) != 0:
            index = max(taxes_ids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        tax.id = id
        tax.taxtype = data['taxtype']
        tax.percentage = data['percentage']
        tax.save()

        return json_format(code = 200, message = "Success")

class AddEmployee(APIView):
    def post(self, request, format=None):
        employees = [employee for employee in Employee.objects.all()]
        employee_id = [int(employee.id) for employee in employees]
        data = request.data

        employee = Employee()
        if len(employee_id) != 0:
            index = max(employee_id) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        employee.id = id
                
        department = Department.objects.get(id=data['department_id'])
        department.numofemployees += 1
        employee.departmentid = department

        tax = Tax.objects.get(id=data['taxid'])
        employee.taxid = tax
        employee.name = data['employee_name']
        employee.phone = data['employee_phone']
        employee.email = data['employee_email']
        employee.address = data['employee_address']
        employee.bankid = data['bankid']
        employee.bankname = data['bankname']
        employee.sex = data['employee_sex']
        employee.exp = data['employee_exp']
        employee.salarydefault = data['employee_salary']
        employee.coef = data['employee_coef']

        employee.save()
        department.save()

        return json_format(code = 200, message = "Success")


class GetEmployee(APIView):
    def get(self, request, format=None):
        data = request.data
        if "employee_id" in data.keys():
            employeeid = data['employee_id']
        else:
            employeeid = None
        employees = getEmployee(employeeid)

        return json_format(code = 200, message = "Success", data = employees)

class DeleteEmployee(APIView):
    def post(self, request, format=None):
        data = request.data
        employee = Employee.objects.get(id=data["employee_id"])
        old_department = Department.objects.get(id=employee.departmentid.id)
        old_department.numofemployees -= 1
        old_department.save()
        employee.delete()
        return json_format(code = 200, message = "Success")

class EditInfoEmployee(APIView):
    def post(self, request, format = None):
        data = request.data
        employee  = Employee.objects.get(id=data['employee_id'])
        tax = Tax.objects.get(id=data['taxid'])
        employee.taxid = tax
        employee.name = data['employee_name']
        employee.phone = data['employee_phone']
        employee.email = data['employee_email']
        employee.bankid = data['bankid']
        employee.bankname = data['bankname']
        employee.address = data['employee_address']
        employee.sex = data['employee_sex']
        employee.exp = data['employee_exp']
        employee.salarydefault = data['employee_salary']
        employee.coef = data['employee_coef']

        old_department = Department.objects.get(id=employee.departmentid.id)
        old_department.numofemployees -= 1
        old_department.save()

        department = Department.objects.get(id=data['department_id'])
        department.numofemployees += 1
        employee.departmentid = department
        
        department.save()
        employee.save()

        return json_format(code = 200, message = "Success")

class AddSalary(APIView):
    def post(self, request, format=None):
        data = request.data
        salaries_id = [int(salary.id) for salary in Salary.objects.all()]

        salary = Salary()
        if len(salaries_id) != 0:
            index = max(salaries_id) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        salary.id = id
        
        salary.fine = data['fine']
        salary.reward = data['reward']

        employee = Employee.objects.get(id=data['employee_id'])
        salary.employeeid = employee

        m, y = [int(i) for i in data['salary_table'].split("/")]
        days = ['{:04d}-{:02d}-{:02d}'.format(y, m, d) for d in range(1, monthrange(y, m)[1] + 1)]
        start_date = datetime.date(*(int(s) for s in days[0].split('-')))
        end_date = datetime.date(*(int(s) for s in days[-1].split('-')))
        total = employee.salarydefault * employee.coef - salary.fine + salary.reward
        salary_tables = [salary_table for salary_table in Salarytable.objects.all()]
        salary_tables_id = [salary_table.id for salary_table in salary_tables]
        exist_salary_table = False
        for salary_table in salary_tables:
            if (start_date == salary_table.startdate) and (end_date == salary_table.enddate):
                exist_salary_table = True
                salary_table.total += total
                salary_table.save()
                salary.salarytableid = salary_table
                break

        if not exist_salary_table:
            salaryTable = Salarytable()
            while True:
                id = randomDigits(8, len(salary_tables))
                if id not in salary_tables_id:
                    salaryTable.id = id
                    break
            salaryTable.note = ""
            salaryTable.startdate = start_date
            salaryTable.enddate = end_date
            salaryTable.total = total
            salaryTable.save()

            salary.salarytableid = salaryTable
        
        salary.save()

        return json_format(code = 200, message = "Success")

class GetSalaryByEmployee(APIView):
    def get(self, request, format=None):
        data = request.data
        salaries = [{'salary_id': salary.id,
                   'employeeid': getEmployee(salary.employeeid.id),
                   'salarytableid': salary.salarytableid.id,
                   'fine': salary.fine,
                   'reward': salary.reward} for salary in Salary.objects.filter(employeeid__id=data['employeeid'])]

        return json_format(code = 200, message = "Success", data = salaries)

class GetSalary(APIView):
    def get(self, request, format=None):
        data = request.data
        if "salaryid" in data.keys():
            salaryid = data['salaryid']
        else:
            salaryid = None
        salaries = getSalary(salaryid)

        return json_format(code = 200, message = "Success", data = salaries)

class GetSalaryTable(APIView):
    def get(self, request, format=None):
        data = request.data

        m, y = [int(i) for i in data['salary_table'].split("/")]
        days = ['{:04d}-{:02d}-{:02d}'.format(y, m, d) for d in range(1, monthrange(y, m)[1] + 1)]
        start_date = datetime.date(*(int(s) for s in days[0].split('-')))
        end_date = datetime.date(*(int(s) for s in days[-1].split('-')))
        
        
        salary_tables = [salary_table for salary_table in Salarytable.objects.all()]
        salary_table_id = None
        for salary_table in salary_tables:
            if (start_date == salary_table.startdate) and (end_date == salary_table.enddate):
                salary_table_id = salary_table.id
                break

        salaries = [{'salary_id': salary.id,
                   'employeeid': getEmployee(salary.employeeid.id),
                   'salarytableid': salary.salarytableid.id,
                   'fine': salary.fine,
                   'reward': salary.reward} for salary in Salary.objects.filter(salarytableid=salary_table_id)]

        return json_format(code = 200, message = "Success", data = salaries)

class EditSalary(APIView):
    def post(self, request, format=None):
        data = request.data
        salary = Salary.objects.get(id=data['salary_id'])
        if "employee_id" in data.keys():
            employee = Employee.objects.get(id=data['employee_id'])
            salary.employeeid = employee
        if "fine" in data.keys():
            salary.fine = data['fine']
        if "reward" in data.keys():
            salary.reward = data['reward']
        salary.save()
        return json_format(code = 200, message = "Success")

class DeleteSalary(APIView):
    def post(self, request, format=None):
        data = request.data
        salary = Salary.objects.get(id=data['salary_id'])
        salary.delete()
        return json_format(code = 200, message = "Success")

class DeleteTax(APIView):
    def post(self, request, format=None):
        data = request.data
        tax = Tax.objects.get(id=data['tax_id'])
        tax.delete()
        return json_format(code = 200, message = "Success")

class EditTax(APIView):
    def post(self, request, format=None):
        data = request.data
        tax = Tax.objects.get(id=data['tax_id'])
        if "taxtype" in data.keys():
            tax.taxtype = data['taxtype']
        if "percentage" in data.keys():
            tax.percentage = data['percentage']
        tax.save()
        return json_format(code = 200, message = "Success")

class GetTax(APIView):
    def get(self, request, format=None):
        data = request.data
        if "taxid" in data.keys():
            taxid = data['taxid']
        else:
            taxid = None
        taxes = getTax(taxid)

        return json_format(code = 200, message = "Success", data = taxes)

class DeleteLog(APIView):
    def post(self, request, format=None):
        data = request.data
        log = Log.objects.get(id=data['log_id'])
        log.delete()
        return json_format(code = 200, message = "Success")

class EditLog(APIView):
    def post(self, request, format=None):
        data = request.data
        log = Log.objects.get(id=data['log_id'])
        if "userid" in data.keys():
            user = User.objects.get(id=data['userid'])
            log.userid = user
        if "name" in data.keys():
            log.name = data['name']
        if "action" in data.keys():
            log.action = data['action']
        if "time" in data.keys():
            log.time = datetime.fromtimestamp(data['time'])
        log.save()
        return json_format(code = 200, message = "Success")

class GetLog(APIView):
    def get(self, request, format=None):
        logs = [{'log_id': log.id,
                   'userid': getUser(log.userid.id),
                   'name': log.name,
                   'action': log.action,
                   'time': log.time} for log in Log.objects.all()]

        return json_format(code = 200, message = "Success", data = logs)

class AddLog(APIView):
    def post(self, request, format=None):
        data = request.data
        logs_id = [int(log.id) for log in Log.objects.all()]

        log = Log()
        if len(logs_id) != 0:
            index = max(logs_id) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        log.id = id
        
        log.time = datetime.datetime.fromtimestamp(data['time'])
        log.name = data['name']
        log.action = data['action']

        user = User.objects.get(id=data['userid'])
        log.userid = user

        log.save()
        return json_format(code = 200, message = "Success")


class TaxStatisticByBranch(APIView):
    def get(self, request, format=None):
        data = request.data
        branchid = data['branchid']
        userid = data['userid']
        taxid = data['taxid']
        if Manager.objects.filter(userid__id = userid).count() == 0:
            return json_format(code = 400, message = "You do not have right to access")
        branch = Branch.objects.get(id = branchid)
        tax = Tax.objects.get(id=taxid)
        if "TNCN" in tax.taxtype:
            time_now = datetime.datetime.now()
            print(time_now.month)

        return json_format(code = 200, message = "Success")

# thông kê các loại thuế
