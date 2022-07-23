import random
import math
import time
from datetime import datetime


def generate():
    dd = str(time.time()) + str(datetime.now())
    randit = str(math.floor(random.random() * 76521969654 + 7685465712))
    value = str(int(randit[0:10]) * int(dd[-6:-1]) * int(dd[0 - 5]))
    account_no = int(value[0:10])
    return account_no
