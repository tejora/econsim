

import random as rand
import sys
#Some simulation paramters

SIMROUNDS = 1000
CUSTOMERCOUNT=100
SELLERCOUNT=10
INITIALCASH=10
SELECTSELLERMODE='ASKFRIENDS'

class Customer:
    def __init__(self, id):
        self.id=id
        self.cash=INITIALCASH
        self.prevSeller = 0

    def demand(self, p):
        return self.cash/p


    def cheapSelect(self, s):
        i=0
        tempseller=0
        sortedSellers = sorted(s, key=lambda x: x.price, reverse = False)
        for seller in sortedSellers:
            seller.demand += self.demand(seller.price)
            if seller.stock>self.demand(seller.price):
                tempseller=seller
                break
        return tempseller

    def selectSeller(self):
        if SELECTSELLERMODE == "ASKFRIEND":
            c=rand.randint(0,CUSTOMERCOUNT-1)
            p=rand.random()
            if p < 0.99:
                return customers[c].prevSeller
            else:
                sellerlist=list()
                for x in xrange(3):
                    s=rand.randint(0,SELLERCOUNT-1)
                    sellerlist.append(sellers[s])
                return self.cheapSelect(s)
        elif SELECTSELLERMODE == 'MOSTFRIENDS':
            
            return 0

        else:
            sellerlist=list()
            for x in xrange(3):
                s=rand.randint(0,SELLERCOUNT-1)
                sellerlist.append(sellers[s])

            return self.cheapSelect(sellerlist)


    def buy(self):
        seller= self.selectSeller( )        
        if seller:
            q=self.demand(seller.price)       
            seller.sell(q)        
            self.prevseller = seller

class Seller:
    def __init__(self, id):
        self.id=id
        self.salesq=0
        self.salesm=0
        self.production=1
        self.price=1
        self.stock=100
        self.demand=1

    def supply(self, p):
        return p  

    def setprod(self):
        if self.demand>self.production:
            self.price += 0.5
        else:
            self.price -= 0.5
        if self.price <0.5:
            self.price=0.5
        self.production=self.supply(self.price)
        self.stock=self.production
        self.demand = 0
        self.salesq = 0
        self.salesm = 0

    def sell(self, q):
        self.salesq += q
        self.salesm += q * self.price
        self.stock -= q



#Initialization

customers=list()
sellers=list()

for x in xrange(CUSTOMERCOUNT):
    customers.append(Customer(x))


for x in xrange(SELLERCOUNT):
    sellers.append(Seller(x))

#Main simulation loop

for x in xrange(SIMROUNDS):

    for s in sellers:
        s.setprod()
        print s.price,
    for c in customers:
        c.buy()
    print x

 

   # print sum(s.price for s in sellers)/float(len(sellers)), ' price %.2f  demand  %.2f stock   %.2f production  %.2f salesq %.2f salesm %.2f' % (sellers[0].price, sellers[0].demand, sellers[0].stock, sellers[0].production, sellers[0].salesq,  sellers[0].salesm )
