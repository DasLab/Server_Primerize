import string
import re

a = ''.join([string.digits, string.ascii_letters,"-(),"])
b = "xxx"

print b.split("@")


pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

str_true = ('test@mail.com',)
            
str_false = ('testmail.com', '@testmail.com', 'test@mailcom','a@a.a')

for t in str_true:
    print (bool(re.match(pattern, t)) == True), '%s is True' %t
for f in str_false:
    print (bool(re.match(pattern, f)) == False), '%s is False' %f