from rest_framework.views import APIView
from rest_framework.response import Response
import random
from .models import *
from .helpers.common import *
import datetime
import numpy as np
from calendar import month_name, monthrange
from .helpers.helpers import *

# bo he so luong, them tong tien luong luc get luong
# them attribute day work
# tinh so tien con lai khi tra them mot truong vao lend hoac loan
# thong ke thue tong
# balance them term (int)

def randomDigits(digits, index):
    lower = 10**(digits-1)
    return lower + index

class ListUsers(APIView):
    def post(self, request, format=None):
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
    def post(self, request, format=None):
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
    def post(self, request, format=None):
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
    def post(self, request, format=None):
        return_data = []
        data = request.data
        if "id" in data.keys():
            productid = data['id']
        else:
            productid = None

        return_data = getProduct(productid)

        return json_format(code = 200, message = "Success", data = return_data)

class GetProductByPartner(APIView):
    def post(self, request, format=None):
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
    def post(self, request, format=None):
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

        list_product = data['list_product']
        number_product = data['number_product']
        list_price = data['list_price']
        products = [Product.objects.get(id = productid) for productid in list_product]
        
        amount = 0
        for price, num in zip(number_product, list_price):
            amount += (price*num)
        doc = Document()
        doc.accountantuserid = user
        docids = [int(doc_.id) for doc_ in Document.objects.all()]
        if len(docids) != 0:
            index = max(docids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        doc.id = id
        doc.type = "bill"
        # doc.time = datetime.datetime.now()
        doc.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        doc.name = data["name"]
        doc.content = data['content']
        doc.amount = amount
        doc.save()

        bill = BuyBill()
        bill.branchid = user.branchid
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
    def post(self, request, format = None):
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
                "documentid": getDocument(bill.documentid.id),
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
        products = [Product.objects.get(id = productid) for productid in list_product]

        amount = 0
        for num, product in zip(number_product, products):
            amount += (product.outprice*num)
        
        doc = Document()
        doc.accountantuserid = user
        docids = [int(doc_.id) for doc_ in Document.objects.all()]
        if len(docids) != 0:
            index = max(docids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        doc.id = id
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
    def post(self, request, format = None):
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
                "documentid": getDocument(bill.documentid.id),
                "customer": bill.customer,
                "cusaddress": bill.cusaddress,
                "cusphone": bill.cusphone,
                "payment": bill.payment,
                "amount": bill.documentid.amount,
                "tax" : getTax(bill.taxid.id)
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
        lendrec.remaining = lendrec.amount
        lendrec.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        lendrec.expired = datetime.datetime.strptime(data['expired'], "%d/%m/%Y")
        lendrec.interest_rate = data['interest_rate']
        lendrec.save()
        return json_format(code = 200, message = "Success")

class GetLend(APIView):
    def post(self, request, format = None):
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
        lendpaying.interestamount = lendrec.amount*lendrec.interest_rate/100
        lendpaying.payingamount = data['payingamount']
        lendrec.remaining = lendpaying.payingamount - lendpaying.interestamount + lendrec.remaining
        lendrec.save()
        lendpaying.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
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
        loanpaying.interestamount = loanrec.amount*loanrec.interest_rate/100
        loanpaying.payingamount = data['payingamount']
        loanrec.remaining = loanpaying.payingamount - loanpaying.interestamount + loanrec.remaining
        loanrec.save()
        loanpaying.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        loanpaying.payment = data['payment']
        loanpaying.save()
        return json_format(code = 200, message = "Success")

class GetLendPaying(APIView):
    def post(self, request, format = None):
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
        loanrecids = [int(loanrec.id) for loanrec in loanrecs]

        loanrec = Loanrec()
        if len(loanrecids) != 0:
            index = max(loanrecids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        loanrec.id = id
        loanrec.chiefmanageruserid = Chiefmanager.objects.get(userid__id = data['userid'])
        loanrec.partnerid = Partner.objects.get(id = data['partnerid'])
        loanrec.desc = data['desc']
        loanrec.amount = data['amount']
        loanrec.remaining = loanrec.amount
        loanrec.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        loanrec.expired = datetime.datetime.strptime(data['expired'], "%d/%m/%Y")
        loanrec.interest_rate = data['interest_rate']
        loanrec.save()

        return json_format(code = 200, message = "Success")

class GetLoan(APIView):
    def post(self, request, format = None):
        data = request.data
        if 'id' in data.keys():
            loanid = data['id']
        else:
            loanid = None
        redata = getLoan(loanid)
        return json_format(code = 200, message = "Success", data = redata)

class GetLoanPaying(APIView):
    def post(self, request, format = None):
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

        investmentrec = Investmentrec()
        if len(investmentrecids) != 0:
            index = max(investmentrecids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        investmentrec.id = id
        investmentrec.chiefmanageruserid = Chiefmanager.objects.get(userid__id = data['userid'])
        investmentrec.desc = data['desc']
        investmentrec.amount = data['amount']
        investmentrec.income = data['income']
        investmentrec.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        investmentrec.type = data['type']
        investmentrec.save()

        return json_format(code = 200, message = "Success")

class GetInvestment(APIView):
    def post(self, request, format = None):
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
            tmp['income'] = investmentrec.income

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
        investmentrec.income = data['income']
        investmentrec.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        investmentrec.type = data['type']
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

        employee.save()
        department.save()

        return json_format(code = 200, message = "Success")


class GetEmployee(APIView):
    def post(self, request, format=None):
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
        salary.workingday = data['workingday']
        employee = Employee.objects.get(id=data['employee_id'])
        salary.employeeid = employee

        m, y = [int(i) for i in data['salary_table'].split("/")]
        days = ['{:04d}-{:02d}-{:02d}'.format(y, m, d) for d in range(1, monthrange(y, m)[1] + 1)]
        start_date = datetime.date(*(int(s) for s in days[0].split('-')))
        end_date = datetime.date(*(int(s) for s in days[-1].split('-')))
        total = computeSalary(salary.employeeid.salarydefault,
                              salary.workingday,
                              WorkingDayPerMonth,
                              salary.fine,
                              salary.reward,
                              salary.employeeid.taxid.percentage/100)
        salary_tables = [salary_table for salary_table in Salarytable.objects.all()]
        salary_tables_id = [int(salary_table.id) for salary_table in salary_tables]
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
            
            if len(salary_tables_id) != 0:
                index = max(salary_tables_id) - 10000000 + 1
            else:
                index = 0
            id = randomDigits(8, index)
            salaryTable.id = id
            salaryTable.note = ""
            salaryTable.startdate = start_date
            salaryTable.enddate = end_date
            salaryTable.total = total
            salaryTable.save()

            salary.salarytableid = salaryTable
        
        salary.save()

        return json_format(code = 200, message = "Success")

class GetSalaryByEmployee(APIView):
    def post(self, request, format=None):
        data = request.data
        salaries = getSalaryByEmployee(data['employeeid'])
        return json_format(code = 200, message = "Success", data = salaries)

class GetSalaryByDepartment(APIView):
    def post(self, request, format=None):
        data = request.data
        salaries = getSalaryByDepartment(data['departmentid'])
        return json_format(code = 200, message = "Success", data = salaries)

class GetSalary(APIView):
    def post(self, request, format=None):
        data = request.data
        if "salaryid" in data.keys():
            salaryid = data['salaryid']
        else:
            salaryid = None
        salaries = getSalary(salaryid)

        return json_format(code = 200, message = "Success", data = salaries)

class GetSalaryTable(APIView):
    def post(self, request, format=None):
        data = request.data

        salaries = getSalaryTable(data['salary_table'])

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
        if "workingday" in data.keys():
            salary.workingday = data['workingday']
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
    def post(self, request, format=None):
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
    def post(self, request, format=None):
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

class SalaryStatisticByBranch(APIView):
    def post(self, request, format=None):
        data = request.data
        branchid = data['branchid']
        userid = data['userid']

        if Manager.objects.filter(userid__id = userid).count() == 0:
            return json_format(code = 400, message = "You do not have right to access")

        return_list = salaryStatisticByBranch(branchid)

        return json_format(code = 200, message = "Success", data = return_list)

class SummarySalaryTable(APIView):
    def post(self, request, format=None):
        salary_tables = [{'salary_table_id': salary_table.id,
                        'total': salary_table.total,
                        'note': salary_table.note,
                        'start_date': salary_table.startdate,
                        'end_date': salary_table.enddate} for salary_table in Salarytable.objects.all()]

        return json_format(code = 200, message = "Success", data = salary_tables)

class SummaryBuyProduct(APIView):
    def post(self, request, format=None):
        data = request.data
        products = getProduct()
        return_data = {}
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        month_bills = {}
        for i in range(1, m+1):
            month_bills["%.2d/%.4d" % (i, y)] = 0
        for product in products:
            product_buy_bills = ProductBuyBill.objects.filter(productid=product['product_id'])
            for bill in product_buy_bills:
                document = bill.buybilldocumentid.documentid
                time = document.time.strftime("%m/%Y")
                if time in month_bills.keys():
                    month_bills[time] += document.amount * product['inprice']
        min = 1e20
        max = -1
        min_month = None
        max_month = None
        statistic = []
        for month, total in month_bills.items():
            statistic.append({"data": month,
                              "value": total})
            if total < min:
                min = total
                min_month = month
            if total > max:
                max = total
                max_month = month
        return_data['statistic'] = statistic
        return_data['max'] = {"data": max_month,
                              "value": max}
        return_data['min'] = {"data": min_month,
                              "value": min}


        return json_format(code = 200, message = "Success", data = return_data)

class SummaryBuyProductByBranch(APIView):
    def post(self, request, format=None):
        data = request.data
        products = [product for product in Product.objects.filter(branchid__id=data['branchid'])]
        return_data = {}
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        month_bills = {}
        for i in range(1, m+1):
            month_bills["%.2d/%.4d" % (i, y)] = 0
        for product in products:
            product_buy_bills = ProductBuyBill.objects.filter(productid=product.id)
            for bill in product_buy_bills:
                document = bill.buybilldocumentid.documentid
                time = document.time.strftime("%m/%Y")
                if time in month_bills.keys():
                    month_bills[time] += document.amount * product.inprice
        min = 1e20
        max = -1
        min_month = None
        max_month = None
        statistic = []
        for month, total in month_bills.items():
            statistic.append({"data": month,
                              "value": total})
            if total < min:
                min = total
                min_month = month
            if total > max:
                max = total
                max_month = month
        return_data['statistic'] = statistic
        return_data['max'] = {"data": max_month,
                              "value": max}
        return_data['min'] = {"data": min_month,
                              "value": min}


        return json_format(code = 200, message = "Success", data = return_data)

class SummarySellProduct(APIView):
    def post(self, request, format=None):
        data = request.data
        products = getProduct()
        return_data = {}
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        month_bills = {}
        for i in range(1, m+1):
            month_bills["%.2d/%.4d" % (i, y)] = 0
        for product in products:
            product_sell_bills = ProductSellBill.objects.filter(productid=product['product_id'])
            for bill in product_sell_bills:
                document = bill.sellbilldocumentid.documentid
                time = document.time.strftime("%m/%Y")
                if time in month_bills.keys():
                    month_bills[time] += document.amount * product['outprice']
        min = 1e20
        max = -1
        min_month = None
        max_month = None
        statistic = []
        for month, total in month_bills.items():
            statistic.append({"data": month,
                              "value": total})
            if total < min:
                min = total
                min_month = month
            if total > max:
                max = total
                max_month = month
        return_data['statistic'] = statistic
        return_data['max'] = {"data": max_month,
                              "value": max}
        return_data['min'] = {"data": min_month,
                              "value": min}


        return json_format(code = 200, message = "Success", data = return_data)

class SummarySellProductByBranch(APIView):
    def post(self, request, format=None):
        data = request.data
        products = Product.objects.filter(branchid__id=data['branchid'])
        return_data = {}

        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        month_bills = {}
        for i in range(1, m+1):
            month_bills["%.2d/%.4d" % (i, y)] = 0
        for product in products:
            product_sell_bills = ProductSellBill.objects.filter(productid=product.id)
            for bill in product_sell_bills:
                document = bill.sellbilldocumentid.documentid
                time = document.time.strftime("%m/%Y")
                if time in month_bills.keys():
                    month_bills[time] += document.amount * product.outprice
        
        min = 1e20
        max = -1
        min_month = None
        max_month = None
        statistic = []
        for month, total in month_bills.items():
            statistic.append({"data": month,
                              "value": total})
            if total < min:
                min = total
                min_month = month
            if total > max:
                max = total
                max_month = month
        return_data['statistic'] = statistic
        return_data['max'] = {"data": max_month,
                              "value": max}
        return_data['min'] = {"data": min_month,
                              "value": min}

        # return_data[product.id] = [month_bills, getProduct(product.id)]


        return json_format(code = 200, message = "Success", data = return_data)

class AddReceipt(APIView):
    def post(self, request, format=None):
        data = request.data
        user = Accountant.objects.get(userid__id=data['userid'])
        receipt = Receipt()

        receipt.receipttype = data['receipttype']
        receipt.desc = data['desc']

        document = Document()
        document.accountantuserid = user    
        docids = [int(doc_.id) for doc_ in Document.objects.all()]
        if len(docids) != 0:
            index = max(docids) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        document.id = id
        document.type = "receipt"
        document.time = datetime.datetime.strptime(data['time'], "%d/%m/%Y")
        document.name = data["name"]
        document.content = data['content']
        document.amount = data['amount']
        document.save()

        receipt.documentid = document
        receipt.save()

        return json_format(code = 200, message = "Success")

class GetReceipt(APIView):
    def post(self, request, format=None):
        data = request.data
        if 'documentid' in data.keys():
            documentid = getDocument(data['documentid'])
        else:
            documentid = None
        receipts = getReceipt(documentid)

        return json_format(code = 200, message = "Success", data=receipts)


# class SummaryReceipt(APIView):
#     def post(self, request, format=None):
#         data = request.data
#         receipts = [receipt for receipt in Receipt.objects.filter(receipttype=data['receipttype'])]
#         total = 0
#         for receipt in receipts:
#             total += receipt.documentid.amount
#         return_data = {data['receipttype']: total}

#         return json_format(code = 200, message = "Success", data = return_data)
# class ProductBuyStatistic(APIView):

class SummaryReceipt(APIView):
    def post(self, request, format=None):
        data = request.data
        return_data = {}

        receipts = [receipt for receipt in Receipt.objects.all()]
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        month_receipt = {}
        for i in range(1, m+1):
            month_receipt["%.2d/%.4d" % (i, y)] = 0
        for receipt in receipts:
            document = receipt.documentid
            time = document.time.strftime("%m/%Y")
            if time in month_receipt.keys():
                month_receipt[time] += document.amount

        min = 1e20
        max = -1
        min_month = None
        max_month = None
        statistic = []
        for month, total in month_receipt.items():
            statistic.append({"data": month,
                              "value": total})
            if total < min:
                min = total
                min_month = month
            if total > max:
                max = total
                max_month = month
        return_data['statistic'] = statistic
        return_data['max'] = {"data": max_month,
                              "value": max}
        return_data['min'] = {"data": min_month,
                              "value": min}


        return json_format(code = 200, message = "Success", data = return_data)

class SummaryReceiptByBranch(APIView):
    def post(self, request, format=None):
        data = request.data
        return_data = {}

        receipts = [receipt for receipt in Receipt.objects.filter(documentid__accountantuserid__branchid=data['branchid'])]
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        month_receipt = {}
        for i in range(1, m+1):
            month_receipt["%.2d/%.4d" % (i, y)] = 0
        for receipt in receipts:
            document = receipt.documentid
            time = document.time.strftime("%m/%Y")
            if time in month_receipt.keys():
                month_receipt[time] += document.amount

        min = 1e20
        max = -1
        min_month = None
        max_month = None
        statistic = []
        for month, total in month_receipt.items():
            statistic.append({"data": month,
                              "value": total})
            if total < min:
                min = total
                min_month = month
            if total > max:
                max = total
                max_month = month
        return_data['statistic'] = statistic
        return_data['max'] = {"data": max_month,
                              "value": max}
        return_data['min'] = {"data": min_month,
                              "value": min}


        return json_format(code = 200, message = "Success", data = return_data)

class TaxStatisticByBranch(APIView):
    def post(self, request, format=None):
        data = request.data
        branchid = data['branchid']
        if "taxid" not in data.keys():
            taxid = None
        taxid = data['taxid']
        return_list = getTaxStatisticByBranch(taxid, branchid)
        return json_format(code = 200, message = "Success", data = return_list)

class StatisticInOutcomeByBranch(APIView):
    def post(self, request, format=None):
        data = request.data
        branchid = data['branchid']
        return_list = dict()
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        tmp_ = {}
        for i in range(1, m+1):
            tmp = getInterestInBranch(branchid, i, y)
            tmp_["%.2d/%.4d" % (i, y)] = tmp
        max = None
        min = None
        maxtype = None
        mintype = None
        for k in return_list.keys():
            print(return_list[k]['interest'])
            if max is None or max < return_list[k]['interest']:
                max = return_list[k]['interest']
                maxtype = k
            if  min is None or min > return_list[k]['interest']:
                min = return_list[k]['interest']
                mintype = k
        return_list["statistic"] = [{"date" : k, "value" : tmp_[k]} for k in tmp_.keys()]
        return_list['max'] = {'type' : maxtype,
                            'value' : max}
        return_list['min'] = {'type' : mintype,
                            'value' : min}
        return json_format(code = 200, message = "Success", data = return_list)

class SalaryStatistic(APIView):
    def post(self, request, format=None):
        return_list = {}
        data = request.data
        # branchs = Branch.objects.all()
        # for branch in branchs:
        #     tmp = salaryStatisticByBranch(branch.id)
        #     return_list[branch.id] = tmp

        max = -1
        min = 99999
        mink = None
        maxk = None
        tmp_ = {}
        for branch in Branch.objects.all():
            tmp = salaryStatisticByBranch(branch.id)['statistic']
            for v in tmp:
                if v['date'] not in tmp_.keys():
                    tmp_[v['date']] = v['value']
                else:
                    tmp_[v['date']] += v['value']
                if v['value'] > max:
                    max = v['value']
                    maxk = v['date']
                if v['value'] < min:
                    min = v['value']
                    mink = v['date']
        return_list["statistic"] = [{"date" : k, "value" : tmp_[k]} for k in tmp_.keys()]
        return_list["min"] = {"ammount" : min, "month" : mink}
        return_list["max"] = {"ammount" : max, "month" : maxk}
        return json_format(code = 200, message = "Success", data = return_list)
        
class StatisticInOutcome(APIView):
    def post(self, request, format=None):
        data = request.data
        branchs = Branch.objects.all()
        return_list = {}
        max = None
        min = None
        maxtype = None
        mintype = None
        for branch in branchs:
            tmp = dict()
            time_now = datetime.datetime.now()
            y, m = time_now.year, time_now.month
            for i in range(1, m+1):
                tmp_ = getInterestInBranch(branch.id, i, y)
                tmp["%.2d/%.4d" % (i, y)] = tmp_
            tmp__ = {}
            for k in tmp.keys():
                if k not in tmp__.keys():
                    tmp__[k] = tmp[k]
                else:
                    tmp__[k] += tmp[k]
        for k in tmp__.keys():
            if max is None or max < tmp__[k]['interest']:
                max = tmp__[k]['interest']
                maxtype = k
            if  min is None or min > tmp__[k]['interest']:
                min = tmp__[k]['interest']
                mintype = k
        return_list["statistic"] = [{"date" : k, "value" : tmp__[k]} for k in tmp__.keys()]
        return_list['max'] = {'type' : maxtype,
                            'value' : max}
        return_list['min'] = {'type' : mintype,
                            'value' : min}
        return json_format(code = 200, message = "Success", data = return_list)

class InvestmentStaistic(APIView):
    def post(self, request, format=None):
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        return_list = {}
        maxincome = -1
        minincome = 99999
        minincometype = None
        maxincometype = None
        maxamount = -1
        minamount = 99999
        minamounttype = None
        maxamounttype = None
        tmp_ = {}
        for i in range(1, m+1):
            investments = Investmentrec.objects.filter(time__year = y, time__month = i)
            sum = 0
            income = 0
            for invest in investments:
                sum += invest.amount
                income += invest.income
            tmp_["%.2d/%.4d" % (i, y)] = {
                "amount" : sum,
                "income" : income
            }
            if maxincome < income:
                maxincome = income
                maxincometype = "%.2d/%.4d" % (i, y)
            if minincome > income:
                minincome = income
                minincometype = "%.2d/%.4d" % (i, y)
            if maxamount < sum:
                maxamount = sum
                maxamounttype = "%.2d/%.4d" % (i, y)
            if minamount > sum:
                minamount = sum
                minamounttype = "%.2d/%.4d" % (i, y)
        return_list["statistic"] = [{"date" : k, "value" : tmp_[k]} for k in tmp_.keys()]
        return_list['maxincome'] = {'type' : maxincometype,
                            'value' : maxincome}
        return_list['minincome'] = {'type' : minincometype,
                            'value' : minincome}
        return_list['maxamount'] = {'type' : maxamounttype,
                            'value' : maxamount}
        return_list['minamount'] = {'type' : minamounttype,
                            'value' : minamount}
        return json_format(code = 200, message = "Success", data = return_list)

class LendStatistic(APIView):
    def post(self, request, format=None):
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        return_list = {}
        max = -1
        min = 99999
        mintype = None
        maxtype = None
        tmp_ = {}
        for i in range(1, m+1):
            lendrecs = Lendrec.objects.filter(time__year = y, time__month = i)
            sum = 0
            for lendrec in lendrecs:
                sum += lendrec.amount
            tmp_["%.2d/%.4d" % (i, y)] = sum
            if max < sum:
                max = sum
                maxtype = "%.2d/%.4d" % (i, y)
            if min > sum:
                min = sum
                mintype = "%.2d/%.4d" % (i, y)
        return_list["statistic"] = [{"date" : k, "value" : tmp_[k]} for k in tmp_.keys()]
        return_list['max'] = {'type' : maxtype,
                            'value' : max}
        return_list['min'] = {'type' : mintype,
                            'value' : min}
        return json_format(code = 200, message = "Success", data = return_list)

class LoanStatistic(APIView):
    def post(self, request, format=None):
        time_now = datetime.datetime.now()
        y, m = time_now.year, time_now.month
        return_list = {}
        max = -1
        min = 99999
        mintype = None
        maxtype = None
        tmp_ = {}
        for i in range(1, m+1):
            loanrecs = Loanrec.objects.filter(time__year = y, time__month = i)
            sum = 0
            for loanrec in loanrecs:
                sum += loanrec.amount
            tmp_["%.2d/%.4d" % (i, y)] = sum
            if max < sum:
                max = sum
                maxtype = "%.2d/%.4d" % (i, y)
            if min > sum:
                min = sum
                mintype = "%.2d/%.4d" % (i, y)
        return_list["statistic"] = [{"date" : k, "value" : tmp_[k]} for k in tmp_.keys()]
        return_list['max'] = {'type' : maxtype,
                            'value' : max}
        return_list['min'] = {'type' : mintype,
                            'value' : min}
        return json_format(code = 200, message = "Success", data = return_list)

class AddBalancerec(APIView):
    def post(self, request, format=None):
        data = request.data
        balances_id = [int(balance.id) for balance in Balancerec.objects.all()]

        balance = Balancerec()
        if len(balances_id) != 0:
            index = max(balances_id) - 10000000 + 1
        else:
            index = 0
        id = randomDigits(8, index)
        
        balance.id = id
        
        accountant = Accountant.objects.get(userid__id=data['accountantuserid'])
        balance.accountantuserid = accountant
        balance.content = data['content']

        balance.amount = data['amount']
        balance.term = data['term']
        
        balance.save()

        return json_format(code = 200, message = "Success")

class GetBalancerec(APIView):
    def post(self, request, format=None):
        data = request.data
        if 'balanceid' in data.keys():
            balanceid = data['balanceid']
        else:
            balanceid = None
        balances = getBalancerec(balanceid)

        return json_format(code = 200, message = "Success", data=balances)

class GetAllTaxStatisticByBranch(APIView):
    def post(self, request, format=None):
        data = request.data
        branchid = data['branchid']
        returndict = getAllTaxByBranch(branchid)
        return json_format(code = 200, message = "Success", data=returndict)

class TaxStatistic(APIView):
    def post(self, request, format=None):
        data = request.data
        taxid = data['taxid']
        returndict = dict()
        max = -1
        min = 99999
        mink = None
        maxk = None
        for branch in Branch.objects.all():
            tmp = getTaxStatisticByBranch(taxid, branch.id)['statistic']
            tmp_ = {}
            for v in tmp:
                if v['date'] not in tmp_.keys():
                    tmp_[v['date']] = v['value']
                else:
                    tmp_[v['date']] += v['value']
                if v['value'] > max:
                    max = v['value']
                    maxk = v['date']
                if v['value'] < min:
                    min = v['value']
                    mink = v['date']
            returndict["statistic"] = [{"date" : k, "value" : tmp_[k]} for k in tmp_.keys()]
        returndict["min"] = {"ammount" : min, "month" : mink}
        returndict["max"] = {"ammount" : max, "month" : maxk}
        return json_format(code = 200, message = "Success", data=returndict)

class AllTaxStatistic(APIView):
    def post(self, request, format=None):
        data = request.data
        returndict = dict()
        max = -1
        min = 99999
        mink = None
        maxk = None
        for branch in Branch.objects.all():
            tmp = getAllTaxByBranch(branch.id)['statistic']
            tmp_ = {}
            for v in tmp:
                if v['date'] not in tmp_.keys():
                    tmp_[v['date']] = v['value']
                else:
                    tmp_[v['date']] += v['value']
                if v['value'] > max:
                    max = v['value']
                    maxk = v['date']
                if v['value'] < min:
                    min = v['value']
                    mink = v['date']
            returndict["statistic"] = [{"date" : k, "value" : tmp_[k]} for k in tmp_.keys()]
        returndict["min"] = {"ammount" : min, "month" : mink}
        returndict["max"] = {"ammount" : max, "month" : maxk}
        return json_format(code = 200, message = "Success", data=returndict)
