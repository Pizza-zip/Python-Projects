import pandas as pd 
import matplotlib.pyplot as plt
import math as m

from scipy.optimize import curve_fit 
import numpy as np 

df =  pd.read_csv( "TESTLAB3.csv", delimiter = ",", names = ["Degree", "Intensity","StandardDivI"])

T = 0
A = 0
P = 0


degree = df["Degree"]
resistance = df["Intensity"]

rad = (degree * m.pi)/180.0

max_guessA = max(rad) 
                      
def sinFit(x,a,b,c,d):
    return (a * np.sin(b*x+c)+d)


pop, constants = curve_fit(sinFit, rad , resistance,p0= [max_guessA,m.pi,3,0.0004], maxfev = 1200, bounds = (0, np.inf))


    
eX,eY,yerr = (rad,resistance, df["StandardDivI"])
plt.errorbar(eX,eY,yerr,mfc = 'black', fmt = "k|")
plt.plot(rad, resistance,"g-",label = 'Experimental Data')
plt.plot

plt.plot(
    rad, sinFit(rad,*pop), "r", label = 'Curve Fit'
)

plt.text(1e-7,1e-4,'1/R = {:.2e}.sin(({:.2e}.x)+{:.2e}) +{:.2e}'.format(pop[0],pop[1],pop[2],pop[3]))


plt.title("Intensity of Laser per degree of Polerizer", color="green", fontsize=20)
plt.xlabel("Radian")  # label x-axis
plt.ylabel("Intensity (W/m^2)")  # label y-axis
plt.legend(loc="upper left")  # show legend at upper left corner of the graph
plt.savefig('intensity Graph')#Save graph to file, change name depending on what you want it to be called
plt.show()  # visualize the plot
    
