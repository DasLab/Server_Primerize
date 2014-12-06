import string
import random

a = ''.join([string.digits, string.ascii_uppercase])
for i in range(10):
	b = ''.join(random.sample(a,6))
	print type(b), b