#!/bin/python

import pandas as pd
import urllib2, json
from pandas import DataFrame
import numpy as np

url = "http://api.census.gov/data/2012/ewks?key=67ab5d61ee001a3432a5915ca6c207bf82e4469f&get=EMP,OPTAX,PAYANN,MSA,RCPTOT&for=county:*&NAICS2012=*"
response = urllib2.urlopen(url)
data = json.loads(response.read())
pd_frame = DataFrame.from_records(data)
print pd_frame.head()
print pd_frame.shape
pd_frame.to_csv("size.income.check.dat",encoding='utf-8',index=False)

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
21. "H012G0002" label="Total !! Owner occupied"
22. "H012G0003" label="Total !! Renter occupied"
23. "P0130003" label="Female: Median Age."
24. "P0130002" label="Male" : Median Age."
25. "P0130001" label="Both sexes" Median Age."
'''
