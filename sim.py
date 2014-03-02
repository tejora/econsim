

import random as rand
import sys
import argparse
#Some simulation paramters




parser = argparse.ArgumentParser(description='Simple market simulation')
parser.add_argument('-n','--simrounds', nargs='?', const=100, default=100, type=int, help='Number of simulation rounds')
parser.add_argument('-c','--customers', nargs='?', const=100, default=100, type=int, help='Number of customers in simulation')
parser.add_argument('-s','--sellers', nargs='?', const=10, default=10, type=int, help='Number of sellers in simulation')
parser.add_argument('-i','--initialcash', nargs='?', const=10, default=10, type=int, help='Amount of cash for each of customer has in the beginning of simulation')
parser.add_argument('-f','--infectionlifetime', nargs='?', const=10, default=10, type=int, help='Only useful with  selectsellermode DISEASE, defines how many rounds consumer is infected')
parser.add_argument('-m','--selectsellermode', nargs='?', const='DEFAULT', default='DEFAULT', choices=['DEFAULT','ASKFRIENDS','DISEASE'], help='How customer selects seller')
args = vars(parser.parse_args())

SIMROUNDS = args['simrounds']
CUSTOMERCOUNT=args['customers']
SELLERCOUNT=args['sellers']
INITIALCASH=args['initialcash']
SELECTSELLERMODE=args['selectsellermode']

INFECTIONLIFETIME=args['infectionlifetime']


class Customer:
    def __init__(self, id):
        self.id=id
        self.cash=INITIALCASH
        self.prevSeller = 0
        self.infectionLife=0

    def demand(self, p):
        return self.cash/p


    def cheapSelect(self, s,n):
        tempseller=0
        slist=list()
        for x in xrange(n):
            c=rand.randint(0,len(s)-1)
            slist.append(s[c])
        #print slist
        sortedSellers = sorted(slist, key=lambda x: x.price, reverse = False)
        for seller in sortedSellers:
            seller.demand += self.demand(seller.price)
       #     print seller.stock, seller.price, self.demand(seller.price)
            if seller.stock>self.demand(seller.price):
                tempseller=seller
                break
            if not tempseller:
                tempseller=sortedSellers[0]
     #   print tempseller
        return tempseller

    def selectSeller(self, customerlist, sellerlist):
        if SELECTSELLERMODE == "ASKFRIENDS":
            c=rand.randint(0,CUSTOMERCOUNT-1)
            p=rand.random()
            if p < 0.6:
                customerlist[c].prevSeller.demand += self.demand(customerlist[c].prevSeller)
                return customerlist[c].prevSeller
            else:
                return self.cheapSelect(sellerlist)
        elif SELECTSELLERMODE == 'DISEASE':
            if self.infectionLife:
                self.infectionLife -= 1
                if self.prevSeller:
                    self.prevSeller.demand += self.demand(self.prevSeller.price)
                return self.prevSeller
            else: 
                contactlist=list()
                for x in xrange(3):
                    c=rand.randint(0,CUSTOMERCOUNT-1)
                    contactlist.append(customerlist[c])
                for c in contactlist:
                    if c.infectionLife:
                        self.infectionLife=INFECTIONLIFETIME
                        if self.prevSeller:
                            c.prevSeller.demand += self.demand(c.prevSeller.price)
                            return c.prevSeller
                        else:
                            return self.cheapSelect(sellerlist,4)
                p=rand.random()
                if p<0.5:
                    self.infectionLife=INFECTIONLIFETIME
                    if self.prevSeller:
                        self.prevSeller.demand += self.demand(self.prevSeller.price)
                        return self.prevSeller
                    else:
                        return self.cheapSelect(sellerlist,4)

            return self.cheapSelect(sellerlist,4)
            

        else:

            return self.cheapSelect(sellerlist,4)


    def buy(self, customerlist, sellerlist):
        seller= self.selectSeller(customerlist, sellerlist )        
     #   print seller,
        if seller:
            q=self.demand(seller.price)       
            if q<seller.stock:
                seller.sell(q)
            else:
                seller.sell(seller.stock)        
            self.prevSeller = seller

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

    def setprod(self, customerlist, sellerlist):
        if self.demand>self.production:
            self.price += 0.2
        else:
            self.price -= 0.2
        if self.price <0.2:
            self.price=0.2
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
        s.setprod(customers, sellers)
        print s.price,
    for c in customers:
        c.buy(customers, sellers)
    
    print x

 

   # print sum(s.price for s in sellers)/float(len(sellers)), ' price %.2f  demand  %.2f stock   %.2f production  %.2f salesq %.2f salesm %.2f' % (sellers[0].price, sellers[0].demand, sellers[0].stock, sellers[0].production, sellers[0].salesq,  sellers[0].salesm )
