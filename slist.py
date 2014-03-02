import random as rand
class aclass:
    def __init__(self, n):
        self.value=10-n
alist=list()
for x in xrange(5):
    alist.append(aclass(x))
print 'first alist'
for x in xrange(len(alist)):
    print x, alist[x], alist[x].value
#slist=()

sortedSellers = sorted(alist, key=lambda x: x.value, reverse = False)


print '2 alist'
for x in xrange(len(alist)):
    print x, alist[x], alist[x].value

print 'sortedlist'
for x in xrange(len(sortedSellers)):
    print x, sortedSellers[x], sortedSellers[x].value

