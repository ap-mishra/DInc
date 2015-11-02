#!/bin/python

import pandas as pd
import urllib2, json
from pandas import DataFrame
import numpy as np

url_p1 = "http://api.census.gov/data/2010/sf1?key="
key = "67ab5d61ee001a3432a5915ca6c207bf82e4469f"
url_params = "&get=NAME,P0190003,P0190004,P0190007,P0190006,P029A001,PCT012H001,PCT012E001,PCT012B001,P029D001,P012C001,H0130002,H0130003,H0130004,H0130005,H0130006,H0130007,H0130008,H0210001,P0120001,H012G0002,H012G0003,P0130003,P0130002,P0130001"

url_p2 = "&for=county:*"
url = url_p1 + key + url_params + url_p2
response = urllib2.urlopen(url)
data = json.loads(response.read())
pd_frame = DataFrame.from_records(data)
pd_frame = pd_frame[pd_frame[0] != 'NAME']
pd_frame.rename(columns = {0: 'County_Name',
                 1:'1P_Male',
                 2:'1P_Female',
                 3:'2P_HusbandWife',
                 4:'2P_Family',
                 5:'White_only',
                 6:'Hispanic_only',
                 7:'Hawaiin_PI_only',
                 8:'Afro_American_only',
                 9:'Asian_only',
                 10:'American_only',
                 11:'1P_HH',
                 12:'2P_HH',
                 13:'3P_HH',
                 14:'4P_HH',
                 15:'5P_HH',
                 16:'6P_HH',
                 17:'7P_HH',
                 18:'Vacant_houses',
                 19:'Total_Pop',
                 20:'Total_Owned',
                 21:'Total_Rented',
                 22:'Female_median_age',
                 23:'Male_median_age',
                 24:'both_sex_median_age',
                 25:'state',
                 26:'county'
                 }, inplace=True)
print pd_frame.head()
print pd_frame.shape

#Process income data from another source table.
#url = "http://api.census.gov/data/2012/ewks?key=67ab5d61ee001a3432a5915ca6c207bf82e4469f&get=EMP,OPTAX,PAYANN,MSA,RCPTOT&for=county:*&NAICS2012=*"
#response = urllib2.urlopen(url)
#data2 = json.loads(response.read())
#income_data = DataFrame.from_records(data2)

#Temp
income_data = pd.read_csv("size.income.check.dat")

#Process state code mapping.
states = pd.read_csv("state_codes.csv")

#Process state and county to match income data.
pd_frame['state'] = pd_frame['state'].apply(int)
pd_frame['county'] = pd_frame['county'].apply(int)

pd_frame = pd.merge(pd_frame, states, on = ['state'])
income_data = pd.merge(income_data, states, on = ['state'])

pd_frame.to_csv("household_data.dat",encoding='utf-8',index=False)
income_data.to_csv("income_data.dat",encoding='utf-8',index=False)


#Doing some validations
x = pd_frame.groupby(['State Name'])['Total_Pop'].sum().reset_index()
x.sort(['Total_Pop'],ascending=False)
#Reveals same numbers as Wikipedia. Validation Complete.



'''
1. ="P0190003" label="1-person household: !! Male householder" 
2. ="P0190004" label="1-person household: !! Female householder"
3. ="Po19007" label="2-or-more-person household: !! Family households: !! Husband-wife family:"
4. ="P0190006" label="2-or-more-person household: !! Family households:"
5. P029A001 : People who are WHITE alone.
6. PCT012H001 : Hispanic or Latino
7. PCT012E001 : Hawaiin or Pacific Islander
8. PCT012B001 : Black or African American
9. P029D001 : People who are Asian alone
10. P012C001 : People who are American or Alaskan Native.
11. "H0130002" label="1-person household"
12. "H0130003" label="2-person household"
13. "H0130004" label="3-person household" 
14. "H0130005" label="4-person household"
15. "H0130006" label="5-person household"
16. "H0130007" label="6-person household"
17. "H0130008" label="7-or-more-person household"
18. H0210001: Vacant houses.
19. ="P0120001" label="Total population"
20. "H012G0002" label="Total !! Owner occupied"
21. "H012G0003" label="Total !! Renter occupied"
22. "P0130003" label="Female: Median Age."
23. "P0130002" label="Male" : Median Age."
24. "P0130001" label="Both sexes" Median Age."
'''
