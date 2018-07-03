#Peephole Optimization
 
import re
import itertools

print("For constant folding example enter the filename as : const_folding_ex1.txt or const_folding_ex2.txt\n ")
print("For Special case instruction example enter the filename as : spcl_case_instr_ex.txt\n")
print("For Operator strength reduction example enter the filename as : opr_strength_reduction_ex.txt\n")
print("For Null sequence reduction example enter the filename as : null_seq_ex.txt\n")
print("For Combined moves example enter the filename as : combined_moves_ex.txt\n")
print("For Indirect moves example enter the filename as : indirect_moves_ex.txt\n")
print("For reordering example enter the filename as : reordering_ex.txt\n")
print("For the demonstration of all the optimization techniques enter the filename as : example_1.txt or example_2.txt\n")


inFile = ""
inFile = input("Enter the file you wish to optimize : ")

with open(inFile,"r") as mfile:
    rcode = mfile.read()
with open(inFile,"r") as mfile:
    code = mfile.read()

def constant_folding(code):

    try:
        op = re.findall('LOC ([0-9]+)\nLOC ([0-9]+)\nMUL', code)
        if op and len(op[0])==2:
            A = int(op[0][0])
            B = int(op[0][1])
            if A!=B:
                code = re.sub('LOC ([0-9]+)\nLOC ([0-9]+)\nMUL', 'LOC ' + str(A * B), code)
        op = re.findall('LOC ([0-9]+)\nLOC ([0-9]+)\nADD', code)
        if op and len(op[0])==2:
            A = int(op[0][0])
            B = int(op[0][1])
            if A!=B:
                code = re.sub('LOC ([0-9]+)\nLOC ([0-9]+)\nADD', 'LOC ' +str(A + B), code)
        op = re.findall('LOC ([0-9]+)\nLOC ([0-9]+)\nSUB', code)
        if op and len(op[0])==2:
            A = int(op[0][0])
            B = int(op[0][1])
            if A!=B:
                code = re.sub('LOC ([0-9]+)\nLOC ([0-9]+)\nSUB', 'LOC ' +str(A - B), code)
        op = re.findall('LOC ([0-9]+)\nLOC ([0-9]+)\nDIV', code)
        if op and len(op[0])==2:
            A = int(op[0][0])
            B = int(op[0][1])
            if A!=B:
                code = re.sub('LOC ([0-9]+)\nLOC ([0-9]+)\nDIV', 'LOC ' +str(((A / B))), code)
      
    finally:
        return code

    

def opr_strength_reduction(code):

    try:
        found = re.findall('LOC 2\nMUL', code)
        if len(found)!=0:
            code = re.sub('LOC 2\nMUL', 'LOC 1\nSHL', code)
        found = re.findall('LOC 2\nDIV', code)
        if len(found)!=0:
            code = re.sub('LOC 2\nDIV', 'LOC 1\nSHR', code)
        found = re.findall('LOC ([0-9]+)\nlLOC 0\nMUL',code)
        if len(found)!=0:
            code = re.sub('LOC ([0-9]+)\nlLOC 0\nMUL', 'LOC 0' ,code)
        opr=1
    finally:
        return code

    
def null_seq(code):
    try:
        code = re.sub('ADI 0\n','', code)
        code = re.sub('BEG 0\n','', code)
        code = re.sub('NEG\nNEG','', code)
        code = re.sub('LOC 0\nADD','', code)
        code = re.sub('LOC 0\nSUB','', code)
        code = re.sub('LOC 1\nMUL','', code)
        code = re.sub('LOC 1\nDIV','', code)
    finally:
        return code



def combined_moves(code):
    try:
        op = re.findall('LOV ([0-9]+)\nLOV ([0-9]+)', code)
        if op and len(op[0])==2:
            A = int(op[0][0])
            B = int(op[0][1])
            if (B-A==2):
                code = re.sub('LOV ([0-9]+)\nLOV ([0-9]+)', 'LDV ' +str(A), code)
        op = re.findall('LDV ([0-9]+)\nLOV ([0-9]+)', code)
        if op and len(op[0])==2:
            A = int(op[0][0])
            B = int(op[0][1])
            if (B-A==4):
                code = re.sub('LDV ([0-9]+)\nLOV ([0-9]+)', 'LAV ' +str(A) + '\nLOI 6', code)
    finally:
        return code



def indirect_moves(code):
    try:
        op = re.findall('LAV ([0-9]+)\nLOI 2', code)
        if op:
            A = int(op[0])
            code = re.sub('LAV ([0-9]+)\nLOI 2', 'LOV ' + str(A), code)
        op = re.findall('LAV ([0-9]+)\nSTI 2', code)
        if op:
            A = int(op[0])
            code = re.sub('LAV ([0-9]+)\nSTI 2', 'STV ' + str(A), code)
    finally:
        return code


def reordering(code):
    try:
        op = re.findall('ADD\nLOC ([0-9]+)\nADD', code)
        if op:
            A = int(op[0])
            code = re.sub('ADD\nLOC ([0-9]+)\nADD', 'LOC ' + str(A) +'\nADD\nADD' , code)
        op = re.findall('ADD\nLOC ([0-9]+)\nSUB', code)
        if op:
            A = int(op[0])
            code = re.sub('ADD\nLOC ([0-9]+)\nSUB', 'LOC ' + str(A) +'\nSUB\nADD' , code)
    finally:
        return code


def special_case_instr(code):
    try:
        op = re.findall('LOC ([0-9]+)\nLOC 1\nADD',code)
        if op:
            A = int(op[0])
            code = re.sub('LOC ([0-9]+)\nLOC 1\nADD','INC '+str(A),code)
        op = re.findall('LOC ([0-9]+)\nLOC 1\nSUB',code)
        if op:
            A = int(op[0])
            code = re.sub('LOC ([0-9]+)\nLOC 1\nSUB','DEC '+str(A),code)

    finally:
        return code



special_case_optimized = special_case_instr(code)
con_fold_optimized = constant_folding(special_case_optimized)
opr_str_optimized = opr_strength_reduction(con_fold_optimized)
null_seq_optimized = null_seq(opr_str_optimized)
combined_moves_optimized = combined_moves(null_seq_optimized)
indirect_moves_optimized = indirect_moves(combined_moves_optimized)
reordering_optimized = reordering(indirect_moves_optimized)


print("\n\nUnoptimized Code"+"\t\t\t\t"+"Optimized Code")
n=reordering_optimized.split("\n")
g=rcode.split("\n")
fl=['\t\t\t\t\t'.join([str(c) for c in x]) for x in itertools.zip_longest(g, n, fillvalue='')]
for i in range(len(fl)):
    print(fl[i])

print("\n\n\n\n\n\n");





