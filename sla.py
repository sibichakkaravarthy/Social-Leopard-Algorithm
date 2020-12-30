import sys
import random
import math
import time

#FITNESS FUNCTION
def fitness(index):
    score = 0
    if ip[index][0] > 10:
        score = score + 20
    if ip[index][1] > 10:
        score = score + 20
    if ip[index][3] >= ip[index][2]:
        score = score + 20
    if ip[index][4] == 1:
        score = score + 20
    if ip[index][5] != "root":
	score = score + 20
    if ip[index][6] > 500:
        score = score + 20
    return score


ip = [[0 for x in range(10)] for y in range(100000)]
with open("ipfile.txt") as f:
    c = 0
    r = 0
    for line in f:
        ip[r][c] = line
	c = c + 1
	if c == 8:
	    r = r + 1
	    c = 0
no_of_f = r


#INITIALIZATION
c1 = 0
c0 = 0
flag = 0
f = 0
threshold = 100
leopards = [0 for x in range(no_of_f)]
leopards[0] = 1
for i in range(1,no_of_f):
    leopards[i] = random.randint(0,1)
    if(leopards[i] == 1):
        c1 = c1 + 1
    else:
        c0 = c0 + 1

c1 = c1 + 1
no_of_p = math.ceil(float(c1)/float(2))
no_of_user = math.ceil(float(c0)/float(2))
no_of_p = int(no_of_p)
no_of_user = int(no_of_user)
mig1 = c1 - no_of_p
mig0 = c0 - no_of_user
migsize = mig0 + mig1

if no_of_user > no_of_p:
    iteration = math.floor(float(no_of_user)/float(no_of_p))
    iteration = int(iteration)
    extra = no_of_user - (iteration*no_of_p)
    if extra != 0:
        col = iteration + 2
    else:
        col = iteration + 1
else:
    col = 2
partition = [[0 for x in range(col)] for y in range(100000)]
mig = [0 for x in range(10000)]
ans = [0 for x in range(10000)]
fit = [[0 for x in range(col)] for y in range(100000)]
mig_fit = [0 for x in range(10000)]

#INITIALIZATION OF TERRITORIES
j = 0
for i in range(no_of_f):
    if j != no_of_p:
        if leopards[i] == 1:
            partition[j][0] = i
            j= j + 1
            leopards[i] = -1

#if no of users <= no of partitions
j = 0
if no_of_user <= no_of_p:
    for i in range(no_of_p):
        partition[i][1] = -1
    for i in range(no_of_f):
        if j != no_of_user:
            if leopards[i] == 0:
                partition[j][1] = i
                j = j + 1
                leopards[i] = -1
#if no of users > no of partitions
if no_of_user > no_of_p:
    for i in range(iteration):
        for j in range(no_of_p):
            for k in range(no_of_f):
                if leopards[k] == 0:
                    partition[j][i+1] = k
                    leopards[k] = -1
                    break
    if extra != 0:
        for i in range(no_of_p):
            partition[i][col-1] = -1
        j = 0
        for i in range(no_of_f):
            if j != extra:
                if leopards[i] == 0:
                    partition[j][col-1] = i
                    j = j + 1
                    leopards[i] = -1

#INITIALIZATION OF MIGRANTS
k = 0
for i in range(no_of_f):
    if k != mig1:
        if leopards[i] == 1:
            mig[k] = i
            k = k + 1
            leopards[i] = -1
k = 0
for i in range(no_of_f):
    if k != mig0:
        if leopards[i] == 0:
            mig[k+mig1] = i
            k = k + 1
            leopards[i] = -1


cc = 0
#while True:
t_end = time.time() + 3 * 1
#cc = cc + 1
while time.time() < t_end:
    cc = cc + 1
    #FITNESS CALCULATION FOR EACH PARTITIONS
    for i in range(0,no_of_p):
        for j in range(0,col):
            if partition[i][j] != -1:
                fit[i][j] = fitness(partition[i][j])

       #FITNESS CALCULATION FOR MIGRANTS
    for i in range(0,migsize):
        if mig[i] != -1:
            mig_fit[i] = fitness(mig[i])
     #USER AND MALICIOUS PROCESS COMPARISON
    for i in range(0,no_of_p):
        for j in range(1,col):
            if fit[i][j] > fit[i][0]:
                for k in range(migsize):
                    if mig[k] == -1:
                        mig[k] = partition[i][0]
                        mig_fit[k] = fit[i][0]
                        flag = 1
                if flag == 0:
                    mig[migsize] = partition[i][0]
                    mig_fit[migsize] = fit[i][0]
                    migsize = migsize + 1
                else:
                    flag = 0
                temp = partition[i][0]
                partition[i][0] = partition[i][j]
                partition[i][j] = temp
                partition[i][j] = -1
                fit[i][0] = fit[i][j]
                fit[i][j] = 0


    #MIGRANT AND TERRITORY COMPARISON
    for i in range(0,migsize):
        for j in range(0,no_of_p):
            if mig_fit[i] > fit[j][0]:
                temp = mig_fit[i]
                mig_fit[i] = fit[j][0]
                fit[j][0] = temp
                temp = mig[i]
                mig[i] = partition[j][0]
                partition[j][0] = temp

        #HIGH FITNESS PROCESS AND MIGRANT COMPARISON
    for i in range(no_of_p):
        for j in range(1,col):
            if fit[i][j] > threshold:
                for k in range(migsize):
                    if mig_fit[k] < fit[i][j]:
                        temp = mig_fit[k]
                        mig_fit[k] = fit[i][j]
                        fit[i][j] = temp
                        temp = mig[k]
                        mig[k] = partition[i][j]
                        partition[i][j] = temp
                        f = 1
                if f == 0:
                    mig[migsize] = partition[i][j]
                    mig_fit[migsize] = fit[i][j]
                    partition[i][j] = -1
                    fit[i][j] = 0
                    migsize = migsize + 1
                else:
                    f = 0
     #MIGRANT FORMING NEW TERRITORIES
    for i in range(migsize):
        if mig_fit[i] > threshold:
            fit[no_of_p][0] = mig_fit[i]
            mig_fit[i] = -1
            partition[no_of_p][0] = mig[i]
            mig[i] = -1
            for j in range(1,col):
                fit[no_of_p][j] = 0
                partition[no_of_p][j] = -1
            no_of_p = no_of_p + 1



#print "iteration: ",cc
print("Processes marked as malicious:")
size = 0
for i in range(0,no_of_p):
    temp = ip[partition[i][0]][7]    
    if temp not in ans:
        ans[size] = temp
        size = size + 1 	
for i in range(0,size):
    print "PID: ",ans[i]    
