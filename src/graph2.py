#!/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#Pre-joint data.
pd_frame = pd.read_csv("household_data.dat")
income_data = pd.read_csv("income_data.dat")

#Graph 2 : Single person household vs. Many person household.

pd_frame['Single_Person'] = pd_frame['1P_Male'] + pd_frame['1P_Female']
pd_frame['OneorMany_Person'] = pd_frame['1P_HH'] + pd_frame['2P_HH'] + pd_frame['3P_HH'] + pd_frame['4P_HH'] + pd_frame['5P_HH'] + pd_frame['6P_HH'] + pd_frame['7P_HH']

x = pd_frame.groupby(['State Name'])['Single_Person'].sum().reset_index()
x2 = pd_frame.groupby(['State Name'])['OneorMany_Person'].sum().reset_index()
x['OneorMany_Person'] = x2['OneorMany_Person']

xplot = x
xplot = xplot[np.isfinite(x['Single_Person'])]
xplot2 = xplot[np.isfinite(xplot['OneorMany_Person'])]

count = range(1,53,1)
s = pd.Series(xplot2['State Name'], name ="State Name")
LABELS = s.tolist()
plt.xticks(count, LABELS, rotation=90)
plt.xlabel('States fpr year 2012')
plt.ylabel('No. of households')
plt.title('Single person households vs rest')

count2 = [x + 0.25 for x in count]

ax = plt.subplot(111)
ax.bar(count,xplot['Single_Person'], align = 'center',color='blue',width=0.25)
ax.bar(count2,xplot2['OneorMany_Person'], align = 'center', color='green',width=0.25)

#Show legend
green_patch = mpatches.Patch(color='green', label='All Household')
blue_patch = mpatches.Patch(color='blue', label='Single Person Household')
plt.legend(handles=[green_patch, blue_patch])
plt.savefig('SinglevsAllHousehold.png')
plt.show()

