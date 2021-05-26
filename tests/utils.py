import random
import string

def random_str(n):
   randlst = [random.choice(string.ascii_lowercase + string.digits) for i in range(n)]
   return ''.join(randlst)
