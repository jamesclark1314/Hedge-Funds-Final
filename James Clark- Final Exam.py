# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 11:21:47 2022

@author: James Clark
"""

import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.stats import skew
from scipy.stats import kurtosis

data = pd.read_csv('FactorReturns_Data.csv')

# Drop the empty columns
data.drop(data.columns[data.columns.str.contains('unnamed',case = False)],
          axis = 1, inplace = True)

# Drop the second row with the additional column label
data = data.drop(data.index[0])

# Create a datetime index
data['Datetime'] = pd.to_datetime(data['Date'], format = '%Y%m')
data = data.set_index(['Datetime'])
del data['Date']

# Convert numeric strings to floats
data = data.astype(float)

# 2

# Create a dataframe containing the factor calculations
factors = pd.DataFrame(index = data.index)
factors['SMB'] = data['Small'] - data['Big']
factors['HML'] = data ['High B/M'] - data['Low B/M']
factors['MOM'] = data ['Winner'] - data['Loser']

# Create a dataframe for the excess returns
excess_rets = pd.DataFrame(index = data.index)

# Compute excess returns for MKT, SMB, HML, & MOM
excess_rets['MKT Exc'] = data['Market'] - data['Risk Free']
excess_rets['SMB Exc'] = factors['SMB'] - data['Risk Free']
excess_rets['HML Exc'] = factors['HML'] - data['Risk Free']
excess_rets['MOM Exc'] = factors['MOM'] - data['Risk Free']
excess_rets['MKT - Fact'] = data['Market'] - data['Risk Free'] - factors[
    'SMB'] - factors['HML'] - factors['MOM']

# Compute the average calandar-month returns for each factor
jan = excess_rets[excess_rets.index.month == 1].mean()
jan = jan.rename('Jan')
feb = excess_rets[excess_rets.index.month == 2].mean()
feb = feb.rename('Feb')

monthly_avg = jan.to_frame().join(feb)

monthly_avg['Mar'] = excess_rets[excess_rets.index.month == 3].mean()
monthly_avg['Apr'] = excess_rets[excess_rets.index.month == 4].mean()
monthly_avg['May'] = excess_rets[excess_rets.index.month == 5].mean()
monthly_avg['Jun'] = excess_rets[excess_rets.index.month == 6].mean()
monthly_avg['Jul'] = excess_rets[excess_rets.index.month == 7].mean()
monthly_avg['Aug'] = excess_rets[excess_rets.index.month == 8].mean()
monthly_avg['Sep'] = excess_rets[excess_rets.index.month == 9].mean()
monthly_avg['Oct'] = excess_rets[excess_rets.index.month == 10].mean()
monthly_avg['Nov'] = excess_rets[excess_rets.index.month == 11].mean()
monthly_avg['Dec'] = excess_rets[excess_rets.index.month == 12].mean()

# 3

# Compute the monthly cumulative return series for the market and the 3 factors
cumrets = pd.DataFrame(index = excess_rets.index)
cumrets['MKT'] = excess_rets['MKT Exc'].cumsum()
cumrets['SMB'] = excess_rets['SMB Exc'].cumsum()
cumrets['HML'] = excess_rets['HML Exc'].cumsum()
cumrets['MOM'] = excess_rets['MOM Exc'].cumsum()
cumrets['MKT - Fact'] = excess_rets['MKT - Fact'].cumsum()

# Plot the cumulative return series for the factors
cumrets.plot(y = ['MKT', 'SMB', 'HML', 'MOM'])
plt.title('Factor Cumulative Returns')
plt.show()

# Calculate the statistics for each factor
mkt_stats = pd.Series(index = ['Avg Yrly Ret', 'Annual Stdev', 'Sharpe','VaR',
                               'Skew', 'Kurtosis'], dtype = 'float64')

mkt_stats['Avg Yrly Ret'] = excess_rets['MKT Exc'].mean() * 12     
mkt_stats['Annual Stdev'] = excess_rets['MKT Exc'].std() * math.sqrt(12)
mkt_stats['Sharpe'] = mkt_stats['Avg Yrly Ret'] / mkt_stats['Annual Stdev']
mkt_stats['VaR'] = excess_rets['MKT Exc'].quantile(0.05)
mkt_stats['Skew'] = skew(excess_rets['MKT Exc'])
mkt_stats['Kurtosis'] = kurtosis(excess_rets['MKT Exc'])

mkt_stats = mkt_stats.rename('MKT')

smb_stats = pd.Series(index = ['Avg Yrly Ret', 'Annual Stdev', 'Sharpe','VaR',
                               'Skew', 'Kurtosis'], dtype = 'float64')

smb_stats['Avg Yrly Ret'] = excess_rets['SMB Exc'].mean() * 12     
smb_stats['Annual Stdev'] = excess_rets['SMB Exc'].std() * math.sqrt(12)
smb_stats['Sharpe'] = smb_stats['Avg Yrly Ret'] / smb_stats['Annual Stdev']
smb_stats['VaR'] = excess_rets['SMB Exc'].quantile(0.05)
smb_stats['Skew'] = skew(excess_rets['SMB Exc'])
smb_stats['Kurtosis'] = kurtosis(excess_rets['SMB Exc'])

smb_stats = smb_stats.rename('SMB')


full_stats = mkt_stats.to_frame().join(smb_stats)

hml_stats = pd.Series(index = ['Avg Yrly Ret', 'Annual Stdev', 'Sharpe','VaR',
                               'Skew', 'Kurtosis'], dtype = 'float64')

hml_stats['Avg Yrly Ret'] = excess_rets['HML Exc'].mean() * 12     
hml_stats['Annual Stdev'] = excess_rets['HML Exc'].std() * math.sqrt(12)
hml_stats['Sharpe'] = hml_stats['Avg Yrly Ret'] / hml_stats['Annual Stdev']
hml_stats['VaR'] = excess_rets['HML Exc'].quantile(0.05)
hml_stats['Skew'] = skew(excess_rets['HML Exc'])
hml_stats['Kurtosis'] = kurtosis(excess_rets['HML Exc'])

hml_stats = hml_stats.rename('HML')

full_stats = full_stats.merge(hml_stats, how = 'left', 
                                  left_index = True, right_index = True)

mom_stats = pd.Series(index = ['Avg Yrly Ret', 'Annual Stdev', 'Sharpe','VaR',
                               'Skew', 'Kurtosis'], dtype = 'float64')

mom_stats['Avg Yrly Ret'] = excess_rets['MOM Exc'].mean() * 12     
mom_stats['Annual Stdev'] = excess_rets['MOM Exc'].std() * math.sqrt(12)
mom_stats['Sharpe'] = mom_stats['Avg Yrly Ret'] / mom_stats['Annual Stdev']
mom_stats['VaR'] = excess_rets['MOM Exc'].quantile(0.05)
mom_stats['Skew'] = skew(excess_rets['MOM Exc'])
mom_stats['Kurtosis'] = kurtosis(excess_rets['MOM Exc'])

mom_stats = mom_stats.rename('MOM')

full_stats = full_stats.merge(mom_stats, how = 'left', 
                                  left_index = True, right_index = True)

# My own strategy - Long only - 50% Market, 50% Momentum
my_strat = pd.DataFrame(columns = ['Rets'])
my_strat['Rets'] = excess_rets['MKT Exc'] * 0.5 + excess_rets[
    'MOM Exc'] * 0.5
my_strat['Cumrets'] = my_strat['Rets'].cumsum()

# Statistics for my strategy
strat_stats = pd.Series(index = ['Avg Yrly Ret', 'Annual Stdev', 'Sharpe','VaR',
                               'Skew', 'Kurtosis'], dtype = 'float64')

strat_stats['Avg Yrly Ret'] = my_strat['Rets'].mean() * 12     
strat_stats['Annual Stdev'] = my_strat['Rets'].std() * math.sqrt(12)
strat_stats['Sharpe'] = strat_stats['Avg Yrly Ret'] / strat_stats['Annual Stdev']
strat_stats['VaR'] = my_strat['Rets'].quantile(0.05)
strat_stats['Skew'] = skew(my_strat['Rets'])
strat_stats['Kurtosis'] = kurtosis(my_strat['Rets'])

strat_stats = strat_stats.rename('My Strat')

full_stats = full_stats.merge(strat_stats, how = 'left', 
                                  left_index = True, right_index = True)

# Add cumulative returns for my strategy to cumrets dataframe
cumrets['My Strat'] = my_strat['Cumrets']

# Plot the cumulative returns for the factors and my strategy
cumrets.plot(y = ['MKT', 'SMB', 'HML', 'MOM', 'My Strat'])
plt.title('Cumulative Returns - Factors vs. My Strategy')
plt.show()

# Function that slices the date and returns a plot of the cumulative returns
def ken_french(start, end):
    frame = cumrets[start:end]
    
    frame.plot(y = ['MKT', 'SMB', 'HML', 'MOM', 'My Strat'])
    plt.title('Cumulative Returns - Factors vs. My Strategy')
    plt.show()

ken_french('1927-01', '1940-12')

# CSV outputs
monthly_avg.to_csv('Monthly Averages.csv')
full_stats.to_csv('Factor Statistics.csv')

# Outputs
print('')
print('MONTHLY AVERAGES')
print('')
print(monthly_avg)
print('')
print('FACTOR STATISTICS')
print('')
print(full_stats)
