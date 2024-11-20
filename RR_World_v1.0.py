#RR World 1.0 (single Fourchier lab)
"""
This program is a Monte Carlo simulation of lab leak risks (output is deaths)
For each year of the simulation, a function determines leak or no leak based on the select agents prior probabilities
If leak is True, then the % global infected and virus case fatality rate are randomly selected
Deaths are then calculated by simple multiplication with the global population
All random selections are from uniform distribution
All model assumptions are taken from Lipsitch and Inglesby (2014 - Moratorium on research intended to create novel
potential pandemic pathogens")
"""

#initialise variables
global_pop=8025000000             #global population assumed 8.025bn people
perc_infect=[0.24, 0.38]          #VAR % global population infected once leak and global spread occurs (airborne influenza assumption)                 #
cfr_range=[0.01, 0.60]            #VAR range of possible case fatality rates
NIAID_prob=[0.05, 0.6]            #VAR upper and lower bound probability of lab leak causing pandemic in any given year based on NIAID data per worker
select_agents_prob=[0.01, 0.12]   #VAR select agents data (2022) prob of lab leak from BSL-3 lab any given year
sim_years=100                     #total number of years simulated (e.g. 100 years)
sample_paths=100                    #total number of alternative histories in Monte Carlo simulation (each history is for 'sim_years')
#Number_labs=100                   #total number of labs (each mutually exclusive risk of leak at above probabilities)

#import packages
import random
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt

#leak/no leak function
def leak():
    roll=random.randint(1,100)
    if roll <= random.uniform(select_agents_prob[0],select_agents_prob[1])*100:    #Using Select Agent Data at present
        #print ('Lab leak occurred')
        return True
    else :
        return False


#Monte Carlo simulations
def science_tm():

#initialise arrays, counter
    deaths_array=[]
    cum_deaths=[]
    years=[]
    year=1
    death_count=0

    while year <= sim_years:

        if leak():                                                  #If lab leak occurs = True
            cfr = random.uniform(cfr_range[0], cfr_range[1])        #calculate case fatality rate
            infect = random.uniform(perc_infect[0], perc_infect[1]) #calculate % global pop infected
            dead = round(global_pop * infect * cfr)                 #calculate deaths
            death_count += dead                                     #update cumulative death tally for this history
            deaths_array.append(dead)                               #update death array
            cum_deaths.append(death_count)                          #update cumulative time series array
            years.append(year)

        else:                                                       #if no lab leak occurs = False
            deaths_array.append(0)                                  #make deaths zero for that year if no leak
            cum_deaths.append(death_count)  # update deaths array with 0 for plotting
            death_count += 0                                        #update cum death tally with 0
            years.append(year)
        year += 1

    #plt.plot(years, np.divide(cum_deaths, 1000000),'k')                #plot each historical sample path (each simulation of 'x' years)
    plt.plot(years,np.divide(cum_deaths,1000000),'k')       #can change to cumulative deaths or deaths_array

x=0
while x < sample_paths:
    science_tm()
    x+=1

#basic stats
#to be inserted

#Figure properties for death per year time series
"""
plt.title('Lab leak deaths - Aerosolized H5N1 - 100 simulations ')
plt.xlabel('Year')
plt.ylabel('Deaths due to Lab Leaks, millions')
plt.show()
"""

#Figure properties for cumulative deaths time series
plt.title('Cumulative Lab leak deaths - Aerosolized H5N1 - 100 simulations ')
plt.xlabel('Year')
plt.ylabel('Cumulative Deaths due to Lab Leaks, millions')
plt.axhline(y=global_pop/1000000,color='r', linestyle='-')
plt.show()




#print(deaths_array) #print whole deaths array for all years simulated
#print('Average annual deaths was:', np.mean(deaths_array))
#print('Largest death event was:',round(max(deaths_array)/1000000,1),'million deaths')



#matplot lib times series of the simulations, showing cumulative deaths? How best to demonstrate?
#runm matplot in separate file

#Need to add additional assumptions around viruses, then introduce matrices in model.