#!/usr/bin/env python3
import sys
import os
import random
import math



# Config Variables
'''Remove the loans.csv file'''
% rm loans.csv # Comment this line if you are not running this in jupyter notebook
               # or know what you are doing. Currently this does not support partial data
                # we have a read_file function but other components need some work

loan_info_file = "loans.csv"

lines_for_each_part = 500
#------
# Constants
''' parts is constant 5 because credit score grades are in 5 parts'''
parts = 5

def is_not_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def read_file(ppl):
    with open(loan_info_file, 'r') as f:
        for l in f.read().split('\n')[1:]:
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
    The Credit Info credit grade that are mapped unto the points defined as follows
    A = 353-400+, 
    B 317-353, 
    C = 281-317, 
    D = 235-281, 
    E = 100-235

    E and D applicants do not get a loan unless it is very small or dep on other factors.
    
    Within grades they also define subgrades that this program does not implement:
    A1 A2 A3 B1 B2 B3 C1 C2 C3 D1 D2 D3 E1 E2 E3
    '''
    
    A,B,C,D,E = 0,1,2,3,4
    
    for i in range(0,parts):
        for j in range(math.ceil(i * lines_for_each_part),  math.ceil((i+1) * lines_for_each_part)):
            
            per = {}

            if i == A:
                if random.randint(0,15) == 1:
                    # Maybe some random people dont get a loan in A
                    per['accepted'] = 0
                    per['health_ins'] = 0
                else:
                    per['accepted'] = 1
                    per['health_ins'] = 1
                per['creditscore'] = random.randint(353,400)
                per['creditgrade'] = 'A'
            elif i == B:
                if random.randint(0,7) == 1:
                    # Maybe some random people dont get a loan in B
                    per['accepted'] = 0
                    per['health_ins'] = 0
                    
                else:
                    per['accepted'] = 1
                    per['health_ins'] = 1
                
                per['creditscore'] = random.randint(317,353)
                per['creditgrade'] = 'B'

            elif i == C:
                n = random.randint(0,1)
                per['accepted'] = n
                per['health_ins'] = n
                per['creditscore'] = random.randint(281,317)
                
                per['creditgrade'] = 'C'

            elif i == D:
                if random.randint(0,3) == 1:
                    per['accepted'] = 1
                    per['health_ins'] = 1
                else:
                    per['accepted'] = 0
                    per['health_ins'] = 0
                
                per['creditscore'] = random.randint(235,281)
                per['creditgrade'] = 'D'

            elif i == E:
                if random.randint(0,40) == 1:
                    # Maybe some random people in E get a loan
                    per['accepted'] = 1
                    per['health_ins'] = 1
                else:
                    per['accepted'] = 0
                    per['health_ins'] = 0
                per['creditscore'] = random.randint(100,235)

                per['creditgrade'] = 'E'
            
            ppl.append(per)


def gen_age(per):
    if per['accepted'] == 1:
        return random.randint(18, 90)
    elif per['creditgrade'] == 'E':
        return random.randint(55,90)
    elif per['creditgrade'] == 'D':
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
    if['creditgrade'] == 'A':
        return random.randint(353,400)
    if['creditgrade'] == 'B':
        return random.randint(317,352)
    if['creditgrade'] == 'C':
        return random.randint(281,316)
    if['creditgrade'] == 'D':
        return random.randint(235,280)
    if['creditgrade'] == 'E':
        return random.randint(100,235)
def gen_amount(per):
    if per['accepted'] == 1:
        if per['age'] > 50 or per['age'] < 25:
            # Small loan half mil to 10 mil
            return random.randint(500000,15000000)
        if per['creditgrade'] == 'E':
            # Small loan
            return random.randint(100000,6000000)
        else:
            # Possibly bigger loan
            return random.randint(1000000,70000000)
    else:
        return random.randint(1000000,100000000)    

def add_to_file(ppl):
    with open(loan_info_file, 'w') as f:
        f.write('accepted,creditscore,amount,age,marital,health_ins,creditgrade\n')
        # Here you can sort the file by other things if you want
        for per in sorted(ppl, key=lambda x: x['accepted']):
            f.write('%s,%s,%s,%s,%s,%s,%s\n' % (per['accepted'], per['creditscore'], per['amount'],per['age'],per['marital'],per['health_ins'],per['creditgrade']))

def main():
    # This list will store a dict for each line
    ppl = []
    
    if is_not_zero_file(loan_info_file):
        print("reading old file...")
        read_file(ppl)
    
    if not ppl:
        create_new(ppl)
        
    for per in ppl:
        '''This is the order in which we will determine each factor
        create_new() handles accepted, creditgrade, health_ins and creditscore'''

        if 'age' not in per:
            per['age'] = gen_age(per)
        if 'marital' not in per:
            per['marital'] = gen_marital(per)
        if 'creditscore' not in per:
            per['creditscore'] = gen_cscore()
        if 'amount' not in per:
            per['amount'] = gen_amount(per)
    
    add_to_file(ppl)
    print("Length of file", loan_info_file, "is:" , len(ppl))
    
main()