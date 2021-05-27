import random
from ..models import *
from datetime import datetime
import numpy as np

def getProduct(productid = None):
    products = [product for product in Product.objects.all()]
    return_data = []
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

    return return_data