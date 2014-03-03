#! /usr/bin/python

from pylab import plot, show, ylim, yticks
import sys
import argparse
import simClass

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

customers=list()
sellers=list()
pricearray=list()

for x in xrange(CUSTOMERCOUNT):
    customers.append(simClass.Customer(x, INITIALCASH, SELECTSELLERMODE, INFECTIONLIFETIME))

for x in xrange(SELLERCOUNT):
    sellers.append(simClass.Seller(x))
    pricearray.append(list())

#Main simulation loop
for x in xrange(SIMROUNDS):
    i=0
    for s in sellers:
        s.setprod(customers, sellers)
        pricearray[i].append(s.price)
        i += 1
    for c in customers:
        c.buy(customers, sellers)
    
for x in pricearray:
    plot(x)
show()


