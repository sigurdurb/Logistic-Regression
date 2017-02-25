#!/usr/bin/env python3
import sys
import os
import random
import math

# Config Variables
loan_info_file = "loans.csv"#sys.argv[1]
total_lines = 1000

def is_not_zero_file(fpath):
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

ppl = []
def read_file():
	with open(loan_info_file, 'r') as f:
		for l in f.read().split('\n')[1:]:
			l = l.strip()
			if not l:
				continue
			l = l.split(',')
			data = {}
			data['accepted'] = l[0]
			if len(l) > 1:
				data['creditscore'] = l[1]
				data['amount'] = l[2]
				data['age'] = l[3]
				data['marital'] = l[4]
			ppl.append(data)

if is_not_zero_file(loan_info_file):
	read_file()
if not ppl:
	# Try to generate evenly distributed 0 and 1 for accepted/not accepted:
	'''
	To help us do that we will be using
	The Credit Info Risk Factor Grade that are defined as follows
	A = 353-400+ points, B 317-353 points, C = 281-317, D = 235-281, E = 100-235
	E and D applicants do not get a loan unless it is very small or dep on other factors.'''
	parts = 5
	A,B,C,D,E = 1,2,3,4,5
	for i in range(0,parts):
		for j in range(math.ceil(i * total_lines),  math.ceil((i+1) * total_lines)):
			data = {}
			if i != D and i != E:
				
				if i == A:
					if random.randint(0,50) == 24:
						# Maybe some random people dont get a loan in A
						data['accepted'] = 0
						
					data['accepted'] = 1
					data['riskf'] = 'A'
					data['creditscore'] = random.randint(353,400)
				if i == B:
					if random.randint(0,25) == 12:
						# Maybe some random people dont get a loan in B
						data['accepted'] = 0
						
					else:
						data['accepted'] = 1
					data['rf'] = 'B'
					data['creditscore'] = random.randint(235,281)

				if i == C:
					data['accepted'] = random.randint(0,1)
					data['creditscore'] = random.randint(100,235)
					data['riskf'] = 'C'
					

			else: # case: D and E
			
				if i == D:
					if random.randint(0,2) == 1:
						data['accepted'] = 1
					else:
						data['accepted'] = 0
					data['riskf'] = 'D'
					data['creditscore'] = random.randint(353,401)

				elif i == E:
					if random.randint(0,80) == 24:
						# Maybe some random people in E get a loan
						data['accepted'] = 1
					else:
						data['accepted'] = 0
					data['riskf'] = 'E'
			print(data)
			ppl.append(data)


def gen_age(per):
	if per['accepted'] == 1:
		return random.randint(18, 90)
	elif data['riskf'] == 'E':
		return random.randint(55,90)
	elif data['riskf'] == 'D':
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
	


with open(loan_info_file, 'w') as f:
	f.write('accepted,creditscore,amount,age,marital')
	# Here you can sort by other things if you want
	for per in sorted(ppl, key=lambda x: x['accepted']):
		f.write('%s,%s,%s,%s,%s\n' % (per['accepted'], per['creditscore'], per['amount'],per['age'],per['marital']))

