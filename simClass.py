import random as rand

class Customer:
    def __init__(self, id, cash, sellermode, infectionlifetime):
        self.id=id
        self.cash=cash
        self.prevSeller = 0
        self.infectionLife=0
        self.sellermode = sellermode
        self.infectionlifetime=infectionlifetime

    def demand(self, p):
        return self.cash/p

    def cheapSelect(self, s,n):
        tempseller=0
        slist=list()
        for x in xrange(n):
            c=rand.randint(0,len(s)-1)
            slist.append(s[c])
        sortedSellers = sorted(slist, key=lambda x: x.price, reverse = False)
        for seller in sortedSellers:
            seller.demand += self.demand(seller.price)
            if seller.stock>self.demand(seller.price):
                tempseller=seller
                break
            if not tempseller:
                tempseller=sortedSellers[0]
        return tempseller

    def selectSeller(self, customerlist, sellerlist):
        if self.sellermode == "ASKFRIENDS":
            c=rand.randint(0,len(customerlist)-1)
            p=rand.random()
            if p < 0.6:
                customerlist[c].prevSeller.demand += \
                    self.demand(customerlist[c].prevSeller)
                return customerlist[c].prevSeller
            else:
                return self.cheapSelect(sellerlist)
        elif self.sellermode == 'DISEASE':
            if self.infectionLife:
                self.infectionLife -= 1
                if self.prevSeller:
                    self.prevSeller.demand += \
                        self.demand(self.prevSeller.price)
                return self.prevSeller
            else: 
                contactlist=list()
                for x in xrange(2):
                    c=rand.randint(0,len(customerlist)-1)
                    contactlist.append(customerlist[c])
                for c in contactlist:
                    if c.infectionLife:
                        self.infectionLife=self.infectionlifetime
                        if self.prevSeller:
                            c.prevSeller.demand += \
                                self.demand(c.prevSeller.price)
                            return c.prevSeller
                        else:
                            return self.cheapSelect(sellerlist,4)
                p=rand.random()
                if p<0.01:
                    self.infectionLife=self.infectionlifetime
                    if self.prevSeller:
                        self.prevSeller.demand += \
                            self.demand(self.prevSeller.price)
                        return self.prevSeller
                    else:
                        return self.cheapSelect(sellerlist,4)
            return self.cheapSelect(sellerlist,4)
        else:
            return self.cheapSelect(sellerlist,4)

    def buy(self, customerlist, sellerlist):
        seller= self.selectSeller(customerlist, sellerlist )        
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
        self.price=10
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



