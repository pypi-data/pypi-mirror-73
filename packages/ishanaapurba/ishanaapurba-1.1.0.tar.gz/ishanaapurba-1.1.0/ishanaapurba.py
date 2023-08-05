""" This is a comment
This to show how comment works
Thi sis ho it works"""

def mylist(mystr,level):
    for item in mystr:
        if isinstance(item,list):
            mylist(item,level+1)
        else:
        	for tabstop in range(level):
        		print ("\t",end="")
        print (item)

mylist1 = [1,2,["hassy",["ram"]]]
mylist (mylist1,0)