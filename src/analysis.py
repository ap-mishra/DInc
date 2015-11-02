#!/bin/python

#Libraries
import pandas as pd
import numpy as np
import math
from geopy.distance import great_circle
from sympy.mpmath import mp

def percent_total(df, col):
    data  = df[col].value_counts(sort=True)
    total = float(df[col].value_counts().sum())
    return data/total

def companies_percent_by_popularity(df, col, rank):
    ranked_data = percent_total(df, col)
    return ranked_data[rank - 1]

def calculate_percentile(df, percentile):
    return np.percentile(np.array(df['Latitude']), percentile)

def max_prob_ratio(df):
    #Conditional probabilities
    a                 = pd.DataFrame(df, columns = ['Borough','Complaint Type'])
    b                 = a.groupby(['Borough','Complaint Type']).size().reset_index()
    b.rename(columns  = {0: 'Size'}, inplace = True)
    b['Cond_Percent'] = b.groupby('Borough')['Size'].transform(lambda x: x/sum(x))

    #Total unconditional prob by complaint type.
    total                = percent_total(data, 'Complaint Type').reset_index()
    total.rename(columns = {'index': 'Complaint Type', 0:'Total_Percent'}, inplace = True)

    #Ratio
    merge          = pd.merge(b, total, on = ['Complaint Type'])
    merge['Ratio'] = (merge['Cond_Percent']/merge['Total_Percent'])
    return merge['Ratio'].max()

def ellipse_area(df):
    lat_mean   = np.mean(data['Latitude'])
    long_mean  = np.mean(data['Longitude'])
    lat_sd     = np.std(data['Latitude'])
    long_sd    = np.std(data['Longitude'])
    mean_point = (lat_mean, long_mean)
    lon_point  = (lat_mean, long_mean + long_sd)
    lat_point  = (lat_mean + lat_sd, long_mean)

    #Great Circle distance
    lat_distance = great_circle(lon_point, mean_point).meters/pow(10,3)
    lon_distance = great_circle(lat_point, mean_point).meters/pow(10,3)

    #Return Area = pi*a*b
    area = (mp.pi * lat_distance * lon_distance)
    return area

def dataload():
    #headertype
    df = pd.read_csv("../data/311_Service_Requests_from_2010_to_Present.csv", parse_dates = [1])
    return df

def remove_unhealthy_vals(df, threshold):
    df['Time'],df['Date'] = df['Created Date'].apply(lambda x:x.time()), df['Created Date'].apply(lambda x:x.date())
    a                     = data.groupby(['Agency'])['Created Date'].value_counts(sort=True).reset_index()
    a.rename(columns      = {0: 'Count', 'level_1': 'Created Date'}, inplace = True)

    # Using this condition to remove records at the exact same value such as 12 AM which indicate data entry issue.
    filtered_data = a[a['Count'] <= threshold][['Agency','Created Date']]
    filtered_list = data.loc[filtered_data.index]
    return filtered_list

def compute_average_callgap(df):
    sorted_list = df['Created Date'].reset_index().sort(ascending=False)
    return np.std(sorted_list['Created Date'] - sorted_list['Created Date'].shift())

def popular_hours(df):
    df['Hour'] = df['Created Date'].apply(lambda x:x.hour)

    a                = df.groupby('Hour')['Hour'].value_counts(sort=True).reset_index()
    a.rename(columns = {0: 'Count', 'level_1' : 'Hour'}, inplace=True)

    final                = df.groupby('Hour')['Date'].value_counts().reset_index()
    final.rename(columns = {0: 'Call Count', 'level_1' : 'Created Date'}, inplace=True)
    #Taking mean as the expected value
    final                = final.groupby(['Hour']).mean()
    fullfinal            = final.reset_index()
    diff                 = fullfinal.max()['Call Count'] - fullfinal.min()['Call Count']

    return diff


if __name__ == "__main__":
    data = dataload()
    #Q1 : Fraction of complaints 
    print("Agency popularity : Rank 2 - ",companies_percent_by_popularity(data, 'Agency', 2))

    #Q2 : Ratio of probabilities
    print("Ratio of probabilities : ",max_prob_ratio(data))

    #Q3 : Latitude
    print("Difference in percentiles : ",calculate_percentile(data, 90) - calculate_percentile(data, 10))

    #Q4 : Area of an ellipse
    print ("Area of one SD ellipse : ",ellipse_area(data))

    #Q5 : Clear unhealthy values
    filtered_data = remove_unhealthy_vals(data, 3)
    std_callgap   = compute_average_callgap(filtered_data)
    print("STDev for call gap = ",std_callgap)

    #Q6 : Difference during popular hours
    diff = popular_hours(filtered_data)
    print("Difference in Call Volume between most popular and least popular houes =",diff)
