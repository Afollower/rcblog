from django.test import TestCase

# Create your tests here.

import math

a = 11
b = 3.0
c = math.floor(a/b)
d = math.trunc(a/b)
e = round(a/b)
print(c)
print(d)
print(e)
