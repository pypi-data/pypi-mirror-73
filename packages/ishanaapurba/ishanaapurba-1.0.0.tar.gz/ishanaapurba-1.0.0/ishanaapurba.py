""" This is a comment
This to show how comment works
Thi sis ho it works"""

def mylist(mystr):
    for item in mystr:
        if isinstance(item,list):
            mylist(item)
        else:
            print (item)
