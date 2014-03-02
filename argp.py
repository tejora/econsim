import sys
import argparse


parser = argparse.ArgumentParser(description='Simple market simulation')

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-f','--foo', nargs='?', const='fff',default='eee', help='Description for foo argument')
args = vars(parser.parse_args())

print args['foo']


