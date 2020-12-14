# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 09:24:42 2020

@author: fghjk
"""
import pandas as pd
import csv
class static(object):
    def __init__(self,filename):
        df=pd.read_csv('db_events.csv')
#        period=dict(df['period'])
#        veh_type=dict(df['veh_type'])
#        mean_speed=dict(df['Mean_SPD'])
#        volume=dict(df['Volume'])
#        site=dict(df['Site'])
#        siteandspeed=df[['Site','Mean_SPD']]
#        siteandvolume=df[['Site','Volume']]
#        periodandveh_type=df[['period','veh_type']]
        for i in range(len(df)):
            df.set_value(i,'t_start',df.xs(i)['t_start'].split(' ')[1].split(':')[0])
#        time_volume=df[['t_start','Volume']]
        #periodandveh_type=self.gather(period,veh_type)
        #hour_volume=self.gather(time,volume)
        #site_volume=self.gather(site,volume)

        """
        statistic of the data
        1. the period and correspond category of the vehicle => for control the curb policy for using
        2. the hour volume
        3. the street and volume statics
        4. the street and the vehicle speed calculation
        """
#        print(df.groupby(by=['Zone','curb_use_type']).size())
#        df.groupby(by=['Zone','Conflict_long']).size().to_csv('test.csv')
        
        #print(periodandveh_type)
        #print(hour_volume)
        #print(site_volume)
        #print(siteandspeed.groupby(by=['Site']).mean())
        #print(siteandvolume.groupby(by=['Site']).mean())
        #print(time_volume.groupby(by=['t_start']).mean())
        #print(periodandveh_type.groupby(by=['period','veh_type']).size())
#        print(df.groupby(by=['Site','loc_type','veh_type']).size())
        dff=df[['Zone','veh_type']]
#        dff=df.loc[(df['Zone'] == '2')& (df['veh_type']=='Large passenger vehicle')]
#        print(dff.groupby(by=['Zone','veh_type']).size().to)
#        print(dff.groupby(by=['Zone','veh_type','event_type']).size())
#        dff=df[['Zone','t_start','event_type']]
#        pauses[pauses["pause_end"] > pauses["pause_start"]]
        dff.groupby(by=['Zone','veh_type']).size().to_frame('size').reset_index().to_csv('zone_vehicle.csv',index=False)
#        result=result[result.groupby(by=['Zone','t_start','veh_type'])['size'].transform('max').eq(result['size'])]
#        result=dff.groupby(by=['Zone','t_start','event_type']).size().to_frame('size').reset_index()
#        print(result)
#        result=result[result.groupby(by=['Zone','t_start'])['size'].transform('max').eq(result['size'])]
#        print(result)
#        result.to_csv('zone_time_max222.csv',index=False)
        
        

#        dff.to_csv('zone_veh_event.csv',index=False)
        
    def gather(self,a,b):
        res={}
        length=len(a)
        for i in range(length):
            cur=str(a[i])+" "+str(b[i])
            if cur not in res.keys():
                res[cur]=1
            else:
                res[cur]+=1
        return res
    def get_actual_peaks(load_df):
        
        """
        Arguments:
            load_df: The entire actual demand datasets.
            Return:
            peaks_df: Keep the highest demand for each day.
            This function keeps the highest demand (the peak hour)
            for each day.
        """
    
        # Create a new column to hold rankings in a day
        rankings = load_df.groupby(['',
                               load_df.ts.dt.date]
                               ).adjusted_demand_MW.rank(ascending=False)
        load_df['rankings_per_day'] = rankings

        mask = load_df['rankings_per_day'] == 1.0
        peaks_df = load_df[mask]

        # Reset index
        peaks_df.reset_index(drop=True, inplace=True)

        return peaks_df

static('db_events.csv')
    


