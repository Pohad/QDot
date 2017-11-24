# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 09:43:15 2017

@author: Oscar
"""
from scipy import *
from pylab import *
import csv

readfile=open('OM Qdot2.txt', 'r')
lines=readfile.readlines()
x=[]
y=[]
for i in lines:
    p=i.split()
    if float(p[0])>=650 and float(p[0])<=800:
        x.append(float(p[0]))
        y.append(float(p[1]))
readfile.close()
plt.figure(1)
plot(x,y)
plt.show()


# define parameters
eGaAs=1.52
c=29987000
f=[c/680.e-9,c/705.e-9,c/735.e-9,c/745.e-9]
#L=1.42*10**(-9) # width in meters
e=1.6*10**(-19) # electron charge
V0=0.22*e # potential well height, in Joule
Esteps=1000 # number of steps in energy vector
E=np.linspace(0,V0,Esteps) # energy vector
m0=9.1*10**(-31) # free electron mass
me=0.067*m0 # effective electron mass
mh=0.48*m0 # effective hole mass
hbar=1.05*10**(-34) # plancks constant

def checkEq1(solE,solH,f):
    a=abs(hbar*f[0]-eGaAs)
    b=solE[0]+solH[0]
    if b-0.01<=a<=b+0.01:
        return True
    return False

listL=linspace(1,10,10000)*1.e-9
for L in listL:
    # Define left and right hand side of (**)
    RHS=np.sqrt((V0-E)/E) # right hand side
    LHSe=np.tan(L/2*np.sqrt(2*me/hbar**2*E));
    LHSh=np.tan(L/2*np.sqrt(2*mh/hbar**2*E));
                                     #print(LHSe, LHSh)
    solE=[]
    solH=[]
    for i in range(len(E)):
        if LHSe[i]-0.01<=abs(RHS[i])<=LHSe[i]+0.01:
            solE.append(RHS[i])
        if LHSh[i]-0.01<=abs(RHS[i])<=LHSh[i]+0.01:
            solH.append(RHS[i])
    #print(solE[0])
    if len(solE)!=0 and len(solH)!=0:
        if checkEq1(solE, solH,f):
            print("found", solE[0],solH[0],L)
    
    
# plot functions, x-axis in electron volts 
plt.figure(2)
plt.plot(E/e,RHS) 
plt.plot(E/e,LHSe)
plt.plot(E/e,LHSh)
plt.ylim([0,1.5])  # set y-axis range
plt.xlim([0,0.22]) # set x-axis range
