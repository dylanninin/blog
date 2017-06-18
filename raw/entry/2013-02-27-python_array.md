---
layout: post
title: Python Array
category : Python
tags : [Python, Libs]
---

Help on module array:

NAME
    array

FILE
    /usr/lib64/python2.6/lib-dynload/arraymodule.so

DESCRIPTION

    This module defines an object type which can efficiently represent
    an array of basic values: characters, integers, floating point
    numbers.  Arrays are sequence types and behave very much like lists,
    except that the type of objects stored in them is constrained.  The
    type is specified at object creation time by using a type code, which
    is a single character.  The following type codes are defined:
    
        Type code   C Type             Minimum size in bytes 
        'c'         character          1 
        'b'         signed integer     1 
        'B'         unsigned integer   1 
        'u'         Unicode character  2 
        'h'         signed integer     2 
        'H'         unsigned integer   2 
        'i'         signed integer     2 
        'I'         unsigned integer   2 
        'l'         signed integer     4 
        'L'         unsigned integer   4 
        'f'         floating point     4 
        'd'         floating point     8 
    
    The constructor is:
    
    array(typecode [, initializer]) -- create a new array
CLASSES
    __builtin__.object
        array
        array
    
    ArrayType = class array(__builtin__.object)
     |  array(typecode [, initializer]) -> array
     |  
     |  Return a new array whose items are restricted by typecode, and
     |  initialized from the optional initializer value, which must be a list,
     |  string. or iterable over elements of the appropriate type.
     |  
     |  Arrays represent basic values and behave very much like lists, except
     |  the type of objects stored in them is constrained.
     |  
     |  Methods:
     |  
     |  append() -- append a new item to the end of the array
     |  buffer_info() -- return information giving the current memory info
     |  byteswap() -- byteswap all the items of the array
     |  count() -- return number of occurrences of an object
     |  extend() -- extend array by appending multiple elements from an iterable
     |  fromfile() -- read items from a file object
     |  fromlist() -- append items from the list
     |  fromstring() -- append items from the string
     |  index() -- return index of first occurrence of an object
     |  insert() -- insert a new item into the array at a provided position
     |  pop() -- remove and return item (default last)
     |  read() -- DEPRECATED, use fromfile()
     |  remove() -- remove first occurrence of an object
     |  reverse() -- reverse the order of the items in the array
     |  tofile() -- write all items to a file object
     |  tolist() -- return the array converted to an ordinary list
     |  tostring() -- return the array converted to a string
     |  write() -- DEPRECATED, use tofile()

     |  Attributes:
     |  
     |  typecode -- the typecode character used to create the array
     |  itemsize -- the length in bytes of one array item


	>>> c = array.array('c','abcdefg')
	>>> h = array.array('H',c.tostring())
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	ValueError: string length not a multiple of item size
	>>> h = array.array('H',c.tostring()+'\x00')
	>>> h
	array('H', [25185, 25699, 26213, 103])

	>>> for i in c.tostring():
	...     print '%s%5d%10s' % (i, ord(i),bin(ord(i)))
	... 
	a   97 0b1100001
	b   98 0b1100010
	c   99 0b1100011
	d  100 0b1100100
	e  101 0b1100101
	f  102 0b1100110
	g  103 0b1100111

	>>> for i in h.tolist():
	...     f = chr(i&0x00ff)
	...     l = chr(i>>8)
	...     print '%s%5d%10s' % (f,ord(f),bin(ord(f)))
	...     print '%s%5d%10s' % (l,ord(l),bin(ord(l)))
	... 
	a   97 0b1100001
	b   98 0b1100010
	c   99 0b1100011
	d  100 0b1100100
	e  101 0b1100101
	f  102 0b1100110
	g  103 0b1100111
	    0       0b
