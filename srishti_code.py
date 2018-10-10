import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt 
#Given l and time t, find out the support and resistance by finding out the time points, through which the lines should pass.    
#col is the input vector of time series. 
# The output is a vector m[0,1,2,3] where m[1] is a list containing the time points so that the support line is obtained by joining (m[1][0],col[m[1][0]]) and (m[1][1], col[m[1][1]]). 
# m[0] gives the distance of CG from the support line. 
# Similarly m[2] gives the distance of CG from the resistance line and m[3] gives the resistance line.

#defining function SnR
def SnR(data,t,l):
	cond1=[[0 for x in range(l+1)] for y in range(l+1)]
	cond2=[[0 for x in range(l+1)] for y in range(l+1)]
	J=0
	m=[0 for x in range(4)]
	x=list(data[t-l:t+1])
#	print("x = ", x)
	g=[t-0.5*l,sum(x)/(l+1)]
#	print("g = ", g)
	m[0]=10**8
	m[2]=10**8
	if l%2==1:
		for i in range(0, math.floor(l/2)+1):
			for j in range(math.floor(l/2)+1,l+1):
				a=np.abs((x[i]-x[j])*g[0]-(i-j)*g[1]+ (x[j]*i-x[i]*j))
#				print("a = ", a)
				b=np.sqrt((x[i]-x[j])**2+(i-j)**2)
#				print("b = ", b)
				J=a/b
#				print("J = ",J)
				C= (x[i]-x[j])/(i-j)
				for k in range (0,l+1):
					if x[k]< x[j]+C*(k-j):
						cond1[i][j]+=1
					elif x[k]== x[j]+C*(k-j):
						cond2[i][j]+=1
#				print(cond1[i][j],cond2[i][j])
				if cond1[i][j]==0:
#					print(J)
					m[0]=min(m[0],J)
					if m[0]==J:
						m[1]=[i,j]
				elif cond1[i][j]+cond2[i][j]==l:
#					print(J)
					m[2]=min(m[2],J)
					if m[2]==J:
						m[3]=[i,j]
	if l%2==0:
		for i in range(0, math.floor(l/2)+1):
			for j in range(math.floor(l/2),l+1):
				if i-j==0:
					cond1[i][j] = 2*l
					cond2[i][j] = 2*l
					continue
				a=np.abs((x[i]-x[j])*g[0]-(i-j)*g[1]+ (x[j]*i-x[i]*j))
#				print("a = ", a)
				b=np.sqrt((x[i]-x[j])**2+(i-j)**2)
#				print("b = ", b)
				J=a/b
#				print("J = ",J)
				C= (x[i]-x[j])/(i-j)
				for k in range (0,l+1):
					if x[k]< x[j]+C*(k-j):
						cond1[i][j]+=1
					elif x[k]== x[j]+C*(k-j):
						cond2[i][j]+=1
#				print(cond1[i][j],cond2[i][j])
				if cond1[i][j]==0:
#					print(J)
					m[0]=min(m[0],J)
					if m[0]==J:
						m[1]=[i,j]
				elif cond1[i][j]+cond2[i][j]==l:
#					print(J)
					m[2]=min(m[2],J)
					if m[2]==J:
						m[3]=[i,j]
	m[1][0]+=t-l
	m[1][1]+=t-l
	m[3][0]+=t-l
	m[3][1]+=t-l
	x1, y1 = m[1],[data[m[1][0]],data[m[1][1]]]
	x2, y2 = m[3],[data[m[3][0]],data[m[3][1]]]
	return [x1,y1,x2,y2]
#calling the functions	

data = pd.read_csv('/home/csjoshi/Documents/SemProject/Datasets/apple_c.csv')
y = data['Close']
l = 40
a1=[]
a2=[]
b1=[]
b2=[]
for t in range(l+1,len(y)-l,math.floor((len(y)-2*l-1)/10)):
	print(t)
	[x1,y1,x2,y2] = SnR(y, t, l)
	print([x1,y1,x2,y2])
	a1.append(x1[0])
	a1.append(x1[1])
	b1.append(y1[0])
	b1.append(y1[1])
	a2.append(x2[0])
	a2.append(x2[1])
	b2.append(y2[0])
	b2.append(y2[1])
x=[]
for i in range(1,len(y)+1):
	x.append(i)
plt.scatter(x,y,color = 'k',s=10)
plt.xlabel('t')
plt.ylabel('St')
plt.plot(a1,b1,label = 'for support')
plt.plot(a2,b2, label = 'for resistance')
plt.legend()
plt.show()
