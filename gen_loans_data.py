#!/usr/bin/env python3
import sys
import os
import random
import math

# Constants
''' Parts is constant 5 because risk factor grades are in 5 parts'''
parts = 5

# Config Variables
'''Remove the loans.csv file'''
% rm loans.csv # Comment this line if you are not running this in jupyter notebook
               # or know what you are doing. Currently this code does not support
               # partial data. That work has started as we have a read_file method but
               # it needs more work.

loan_info_file = "loans.csv"

lines_for_each_part = 200
#------

def is_not_zero_file(fpath):
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def read_file(ppl):
	with open(loan_info_file, 'r') as f:
		for l in f.read().split('\n')[1:]:
			print(l)
			l = l.strip()
			if not l:
				continue
			l = l.split(',')
			per = {}
			per['accepted'] = l[0]
			if len(l) > 1:
				per['creditscore'] = l[1]
				per['amount'] = l[2]
				per['age'] = l[3]
				per['marital'] = l[4]
            
			ppl.append(per)

def create_new(ppl):

	# Try to generate evenly distributed 0 and 1 for accepted/not accepted:
	'''
	To help us do that we will be using
	The Credit Info Risk Factor Grade that are defined as follows
	A = 353-400+, 
	B 317-353, 
	C = 281-317, 
	D = 235-281, 
	E = 100-235

	E and D applicants do not get a loan unless it is very small or dep on other factors.
	'''
	
	A,B,C,D,E = 0,1,2,3,4
	
	for i in range(0,parts):
		for j in range(math.ceil(i * lines_for_each_part),  math.ceil((i+1) * lines_for_each_part)):
			
			per = {}

			if i == A:
				if random.randint(0,50) == 24:
					# Maybe some random people dont get a loan in A
					per['accepted'] = 0
					
				per['accepted'] = 1
				per['creditscore'] = random.randint(353,400)
				per['riskf'] = 'A'
			elif i == B:
				if random.randint(0,25) == 12:
					# Maybe some random people dont get a loan in B
					per['accepted'] = 0
					
				else:
					per['accepted'] = 1
				
				per['creditscore'] = random.randint(317,353)
				per['riskf'] = 'B'

			elif i == C:
				per['accepted'] = random.randint(0,1)
				per['creditscore'] = random.randint(281,317)

				per['riskf'] = 'C'

			elif i == D:
				if random.randint(0,2) == 1:
					per['accepted'] = 1
				else:
					per['accepted'] = 0
				
				per['creditscore'] = random.randint(235,281)
				per['riskf'] = 'D'

			elif i == E:
				if random.randint(0,80) == 24:
					# Maybe some random people in E get a loan
					per['accepted'] = 1
				else:
					per['accepted'] = 0
				per['creditscore'] = random.randint(100,235)

				per['riskf'] = 'E'
			
			ppl.append(per)


def gen_age(per):
	if per['accepted'] == 1:
		return random.randint(18, 90)
	elif per['riskf'] == 'E':
		return random.randint(55,90)
	elif per['riskf'] == 'D':
		if random.randint(0,4) == 2:
			return random.randint(18,30)
		return random.randint(55,90)
	else:
		return random.randint(18, 90)

def gen_marital(per):
	if per['age'] > 78:
		return 0
	if per['accepted'] == 1:
		if random.randint(0,6) == 3:
			return 0
		else:
			return 1
	if per['accepted'] == 0:
		if random.randint(0,2) == 1:
			return 1
		else:
			return 0

def gen_cscore(per):
	'''We will be basing the credit score the risk factor 
	The Credit Info Risk Factor Grade that are defined as follows
	A = 353-400+ points, B 317-353 points, C = 281-317, D = 235-281, E = 100-235'''
	if['riskf'] == 'A':
		return random.randint(353,400)
	if['riskf'] == 'B':
		return random.randint(317,352)
	if['riskf'] == 'C':
		return random.randint(281,316)
	if['riskf'] == 'D':
		return random.randint(235,280)
	if['riskf'] == 'E':
		return random.randint(100,235)
def gen_amount(per):
	if per['accepted'] == 1:
		if per['age'] > 50 or per['age'] < 25:
			# Small loan half mil to 10 mil
			return random.randint(500000,15000000)
		if per['riskf'] == 'E':
			# Small loan
			return random.randint(100000,6000000)
		else:
			# Possibly bigger loan
			return random.randint(1000000,70000000)
	else:
		return random.randint(1000000,100000000)	

def add_to_file(ppl):
	with open(loan_info_file, 'w') as f:
		f.write('accepted,creditscore,amount,age,marital\n')
		# Here you can sort the file by other things if you want
		for per in sorted(ppl, key=lambda x: x['accepted']):
			f.write('%s,%s,%s,%s,%s\n' % (per['accepted'], per['creditscore'], per['amount'],per['age'],per['marital']))

def main():
    # This list will store a dict for each line
    ppl = []
    
    if is_not_zero_file(loan_info_file):
        read_file(ppl)
    
    if not ppl:
        create_new(ppl)
        
    for per in ppl:
        '''This is the order in which we will determine each factor'''
        if 'age' not in per:
            per['age'] = gen_age(per)
        if 'marital' not in per:
            per['marital'] = gen_marital(per)
        if 'creditscore' not in per:
            per['creditscore'] = gen_cscore()
        if 'amount' not in per:
            per['amount'] = gen_amount(per)
    
    print("Length of file", loan_info_file, "is:" , len(ppl))
    
main()