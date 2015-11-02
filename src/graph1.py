#!/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#matplotlib inline

#Pre-joint data.
pd_frame = pd.read_csv("household_data.dat")
income_data = pd.read_csv("income_data.dat")

#Graph 1 : State by Salary and income generated.

income_data['PerCapitaSalary'] = income_data['PAYANN']*1000/income_data['EMP']
x = income_data.groupby(['State Name','NAICS2012'])['PerCapitaSalary'].mean().reset_index()
income_data['RCPTOT_perEmployee'] = income_data['RCPTOT']*1000 / income_data['EMP']
x2 = income_data.groupby(['State Name','NAICS2012'])['RCPTOT_perEmployee'].mean().reset_index()

x['RCPTOT'] = x2['RCPTOT_perEmployee']

#Filtering only to Technology jobs
xplot = x[x['NAICS2012'] == '54']
xplot = xplot[np.isfinite(x['PerCapitaSalary'])]
xplot2 = xplot[np.isfinite(xplot['RCPTOT'])]


#table.to_csv("table.csv", index=False, encoding='utf-8')
count = range(1,40,1)
s = pd.Series(xplot2['State Name'], name ="State Name")
LABELS = s.tolist()
#plt.xticks(count, LABELS, rotation=90)

count2 = [x + 0.25 for x in count]
count3 = [x - 0.25 for x in count]

print count2

fig, axes = plt.subplots(ncols=2, sharey=True)

axes[0].barh(count, xplot['PerCapitaSalary'], align='center', color='gray')
axes[0].set(title='Per Capita Salary')
axes[1].barh(count, xplot['PerCapitaSalary']/(xplot2['RCPTOT']), align='center', color='gray')
axes[1].set(title='% of Per Capita Salary to his Revenue contribution')
axes[0].invert_xaxis()
axes[0].set(yticks=count, yticklabels=LABELS)
axes[0].yaxis.tick_right()

#plt.setp(plt.xticks()[0], rotation=90)
plt.setp(plt.xticks()[1], rotation=60)

fig.tight_layout()
fig.subplots_adjust(wspace=0.59)
plt.savefig('SalariesbyState.png')

plt.show()

