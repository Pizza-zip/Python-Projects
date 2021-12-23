# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import sympy as smp
import matplotlib.pyplot as plt
from scipy.integrate import quad #calculates numerical integral returning; integral[0], estimated error[1]

#Definite integral

x = smp.symbols('x', real = True) #define variable x for integration
a, b = smp.symbols('a b', real=True, positive=True) #defines variables, as real, positive number
f = smp.cos(b*x)*smp.exp(-a*x) #defines function f (can be whatever function you may want)

smp.integrate(f,x) #integrates function 'f' wtih respect to x
smp.integrate(f, (x,0,smp.oo)) #integrates function 'f' with respect to x from 0 to infinity
# use eval.f() to evaluate integral as float

#Solving integral for a range of values of c,d
#Define function 'g' having variable 'x' and constants c,d
def g(x,c,d): 
    return 1/((c-np.cos(x))**2 + (d-np.sin(x))**2)

#Define arrays for c,d having values ranging from 0 to 20, increasing by 1
c_array = np.arange(0,20,1)
d_array = np.arange(0,20,1)

#Define array 'integrals' which contains value of c,d and value of integral. [0] allows for only value of integral to be stored in array
#followed by list comprehension to calculate all values in c/d _array

integrals = [[c, d, quad(g, 0, 2*np.pi, args=(c, d))[0]] for c in c_array for d in d_array]

