#!/usr/bin/python

import csv
import time  # This is required to include time module.
from datetime import date
import string
import random



#Basic
print("-- Basic " + "-" + " Python --")
tuple = ( 'abcd', 786 , 2.23, 'john', 70.2  )
tinytuple = (123, 'john')

#Array
print(tuple)           # Prints complete list
print("-- Array slice --")
print(tuple[0])        # Prints first element of the list
print(tuple[1:4])      # Prints elements starting from 2nd till 3rd
print(tuple[2:])       # Prints elements starting from 3rd element
print(tinytuple * 2)   # Prints list two times
#print tuple + tinytuple # Prints concatenated lists
newthing = tinytuple + tuple[:4];
print(newthing)
array_val = [1,2,3,4,5,6,7]
print(array_val[:3:2]) #start:end:skip
print(array_val[50:11]) # index fail

print("-- Dict --")
doclisttt = {'A': 1, 'B': 2, 'C': 3,
             'D': 1, 'E': 2, 'F': 3}
anotherdict = dict(Ax = 1, Bx = 2, Cx = 3)

count = doclisttt['A'] + doclisttt['B'] + doclisttt['C']
print(count)
count = anotherdict['Ax'] + anotherdict['Bx'] + anotherdict['Cx']
print(count)
print(anotherdict['Ax'])

print("-- String --")
city = "this is a city"
print(city)
sub_city = city[0:4]
print(sub_city)
print(len(sub_city))

print("-- Convert --")
abc = '123'
print(abc)
print(repr(abc))
print(type(abc))
bcd = int(abc)
print(bcd)
print(repr(bcd))
print(type(bcd))
cde = float(abc)
print(cde)
print(repr(cde))
print(type(cde))
list_abc = list(abc)
print(list_abc)
print(repr(list_abc[1]))

print("-- Class --")
class xyz:
    x = None
    y = None
    z = None

xyz_dat = xyz()
xyz_dat.x = 11;
xyz_dat.y = 'A';
xyz_dat.z = "AAAA";

print("x:" + str(xyz_dat.x) + " y:" + str(xyz_dat.y) + " z:" + str(xyz_dat.z))

mystring = 'string'
for i in range(11):
    mystring +=repr(i)
print(mystring)

print("Find 'city' in the string " + repr(city) + "... found at index " +  str(city.find('city')))

# print "-- Input --"
# name = raw_input("Enter name: ");
# print name
# val = input("Enter val: ");
# print val

print("-- Loop --")
it_num = range(3,10)
for num in it_num:
    if num % 2 == 0:        # check even
        print(num,end=" ")  # print without newlines
    elif num == 7:
        break

for num in it_num:
    print(num,end=" ")  # print without newlines
else:
    print("num reached: " + str(num))

item = 0
while item < 22:
    print(item)
    item += 1
else:
    print("item reached: " + str(item))


ticks = time.time()
print("Number of ticks since 12:00am, January 1, 1970: " + str(ticks))
print(date.today())

ddd = None
print(ddd is None)

print("-- Function --")
def random_word(text):
    word = text.split(' ')
    #random.sample(string.ascii_uppercase,10)
    print(word)

random_word("this is my word")