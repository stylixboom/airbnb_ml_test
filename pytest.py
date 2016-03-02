#!/usr/bin/python

import csv

#Basic
print "-- Basic " + "-" + " Python --"
tuple = ( 'abcd', 786 , 2.23, 'john', 70.2  )
tinytuple = (123, 'john')

#Array
print tuple           # Prints complete list
print "-- Array slice --"
print tuple[0]        # Prints first element of the list
print tuple[1:4]      # Prints elements starting from 2nd till 3rd
print tuple[2:]       # Prints elements starting from 3rd element
print tinytuple * 2   # Prints list two times
#print tuple + tinytuple # Prints concatenated lists
newthing = tinytuple + tuple[:4];
print newthing

print "-- Dict --"
doclisttt = {'A': 1, 'B': 2, 'C': 3,
             'D': 1, 'E': 2, 'F': 3}
anotherdict = dict(Ax = 1, Bx = 2, Cx = 3)

count = doclisttt['A'] + doclisttt['B'] + doclisttt['C']
print count
count = anotherdict['Ax'] + anotherdict['Bx'] + anotherdict['Cx']
print count

print "-- String --"
city = "this is a city"
print city
sub_city = city[:5]
print sub_city

