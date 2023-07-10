"""
Created on Sat Jun 24 14:56:48 2023

@author: amhar
"""

# from underground import *
# from underground.cli.findstops import *
# import underground.feed
from underground.models import SubwayFeed
import os
from pandas import read_csv
from pytz import timezone as tz
from datetime import datetime
#############
### FLAGS ###
#############
needLUT=False
#################
##GLOBAL VARS####
#################
newYorkTz = tz("America/New_York")
API_KEY = 'TdfMPEIzV26MOcndtJN0j3igqthjPNFS4flMBhEE' #API key to access MTA API
feed_M = SubwayFeed.get('M',api_key=API_KEY)
feed_L = SubwayFeed.get('L',api_key=API_KEY)
feed_J = SubwayFeed.get('J',api_key=API_KEY)

# Mstops = feed_M.extract_stop_dict().get('M',dict())
# Lstops = feed_L.extract_stop_dict().get('L',dict())
# Jstops = feed_J.extract_stop_dict().get('J',dict())

stops={'Myrtle':['M11N','Myrtle Av'],
       'Morgan':['L14N','Morgan Av'],
       'MyrtleJ':['M11S','Myrtle Av']}

if needLUT:
    file_path = os.path.realpath(__file__)
    station_file = os.path.join(os.path.dirname(file_path),'Stations.csv')
    stations_LUT = read_csv(station_file, sep=',',usecols=[i for i in range(9)])


def get_stopID(stop_string):
    stopID = stations_LUT[stations_LUT['Stop Name'] == stop_string]['GTFS Stop ID'].values[0]
    return stopID

def get_stop_name(stopID):
    stopname = stations_LUT[stations_LUT['GTFS Stop ID'] == stopID]['Stop Name'].values[0]
    return stopname

def get_L_live_info(Lfeed):
    all_Lstops = Lfeed.extract_stop_dict().get('L',dict())
    morganAv = all_Lstops['L14N']
    return morganAv

def get_M_live_info(Mfeed):
    all_Lstops = Mfeed.extract_stop_dict().get('M',dict())
    myrtleAv = all_Lstops['M11N']
    return myrtleAv

def get_J_live_info(Jfeed):
    all_Lstops = Jfeed.extract_stop_dict().get('J',dict())
    myrtleAv = all_Lstops['M11S']
    return myrtleAv

#### TODO: do Z stops too when running


# liveMorg = get_L_live_info(feed_L)
# liveMyrtl = get_M_live_info(feed_M)
# liveMyrtlJ = get_J_live_info(feed_J)

def demo_both():
    now = datetime.now(newYorkTz)
    live_Myrtle_J = get_J_live_info(feed_J)
    live_Myrtle_M = get_M_live_info(feed_M)
    live_Morgan = get_L_live_info(feed_L)
    arrivals_J = [int(round((i-now).total_seconds()/60)) for i in live_Myrtle_J]
    arrivals_J = [j for j in arrivals_J if ((j>0) and (j<30))]
    arrivals_M = [int(round((i-now).total_seconds()/60)) for i in live_Myrtle_M]
    arrivals_M = [j for j in arrivals_M if ((j>0) and (j<30))]
    arrivals_L = [int(round((i-now).total_seconds()/60)) for i in live_Morgan]
    arrivals_L = [j for j in arrivals_L if ((j>0) and (j<30))]
    print('Next Myrtle Ave J trains are in (min): {}'.format(arrivals_J))
    print('Next Myrtle Ave M trains are in (min): {}'.format(arrivals_M))
    print('Next Morgan Ave L trains are in (min): {}'.format(arrivals_L))
    
    return arrivals_J
test = demo_both()
