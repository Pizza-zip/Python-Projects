#Import all necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import math 

#call specific functions
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from scipy.optimize import curve_fit

#Define coloum names
colNames = ['FL','CL','PMD'] #where FL = Fiber Loss, CL = cable length, PMD = Polarization mode dispersion

#Call data from excel file
data = pd.read_excel("fiber_data.xlsx", names = colNames, header=0)

#Seperate data by coloums into each of there own variables
FL = data['FL']
CL = data['CL']
PMD = data['PMD']


# Avg fiber loss
avg = sum(FL)/len(FL) #calculate the average fiber loss
FLS = FL.sort_values() #sort the FL values in increasing order 
p = np.percentile(FLS,90) #calculate the 90th percentile




#Loss Coeficient 
lossCoef = np.gradient(FL,CL) #calculate the derivative of FL with rescpet to CL so we get a rate of change with units dB/km

avgLoss = sum(lossCoef)/len(lossCoef) #calculate the average loss coeficient 
standardLoss = np.std(lossCoef, axis = None) #calculate the standard deviation of the loss coefcient 

maxLoss = np.amax(lossCoef) #Calculate maximum value
minLoss = np.amin(lossCoef) #Calculate minimum value
divDistance = (maxLoss - avgLoss)/standardLoss #calculate the amount of standard Div from the mean the maximum is 



#Histogram
#Calculating the correct value for bins using the Freedman-Diaconis rule
#https://en.wikipedia.org/wiki/Freedman–Diaconis_rule
q25, q75 = np.percentile(CL, [25, 75]) #calculating the 25 and 75 percentile from CL
bin_width = 2 * (q75 - q25) * len(CL) ** (-1/3) #using Freedman-diaconis rule to calculate the bin width
bins = round((CL.max() - CL.min()) / bin_width) #calculating the number of bins



fig, ax = plt.subplots() #Define plot

ax.hist(CL,density=True, bins=bins,label="Data") #defines histogram
ax.set(xlabel = 'Cable Length (km)', ylabel = 'Precentage', title = 'Distribution of fiber Length') #define axes
mn,mx = plt.xlim() #define limits
plt.xlim(mn,mx) #plot limits
kde_xs = np.linspace(mn,mx,300) #define the kernal
kde = st.gaussian_kde(CL) #define the gaussian of CL
plt.plot(kde_xs, kde.pdf(kde_xs), label ='Gaussian Fit') #Plot the gaussian curve
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1)) #set yaxis as precentage
plt.legend(loc='best')
plt.show() #show plot


#PMD vs Length Graphs

#Generalized Logistic
#https://en.wikipedia.org/wiki/Generalised_logistic_function
def fivepl(x, a, b, c, d, g):
    return ( ( (a-d) / ( (1+( (x/c)** b )) **g) ) + d )
# a is the lower asymptote 
# b is the growth rate (rate of dispersion with respect to km)
# c is the inflection point of the curve 
# d is the upper asymptote
# g is the asymmetry factor


popt, pcov = curve_fit(fivepl, CL, PMD, maxfev = 2000) #use curve_fit function

fig, axs = plt.subplots() #define plot

axs.plot(CL,PMD, label ='Data') #plot data CL & PMD
axs.set(xlabel = 'Cable Length (km)', ylabel = 'Polarization mode dispersion ',title = 'Polarization mode Dispersion vs Cable length') #define axis
plt.plot(CL, fivepl(CL,*popt), "r", label = 'Curve Fit') #plot curve fit
plt.legend(loc='best')
plt.show()
#Printing results

print("The average fiber loss is" , avg , "dB")
print("The 90th percintile is" ,p , "dB")
print("the Average loss coeficient is", avgLoss, "dB/km")
print("The standard deviation of the loss coeficient is", standardLoss)
print("The max Loss is", maxLoss, "dB/km. The min loss is ", minLoss, "dB/km")
print("The maximum is", divDistance, "standard deviations from the mean.")
print("Freedman–Diaconis number of bins:", bins)
print("The fit parameters are; a = ", popt[0], "b = ",popt[1], "c = ", popt[2], "d = ", popt[3],"g = ", popt[4])