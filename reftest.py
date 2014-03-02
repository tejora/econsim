a=list()

a.append('a')
a.append('b')
a.append('c')
a.append('d')

print a

b=list()

#b.append(a[3])
#b.append(a[2])
b.append(a)
b.append([1,2,3])
print b

a[3]=2

print a
print b


