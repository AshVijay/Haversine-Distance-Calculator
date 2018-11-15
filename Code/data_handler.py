import pandas as pd
from math import *
import data_loader
import create_kml
import numpy as np

def calc_POI(image_dataframe,filename,distance):
#Function to retrieve images near the Points of interest
    POI_dataframe = data_loader.Read_POI(filename)
    return(calc_Distance(POI_dataframe.loc[:,['name','Lat','Long','Alt']], image_dataframe,distance))

def calc_Distance(video_dataframe , image_dataframe, distance):
#Calculating the ground distance between two coordinates using the Haversines formula
#Then approximating a Euclidean distance including the altitude parameter
      print("\n\n" + "....Calculating haversine distances for the entire data set......"+"\n\n")
      final_list=[]
      for index1,rows1 in video_dataframe.iterrows():
            image_list= []
            for index2,rows2 in image_dataframe.iterrows():
                if (haversine( float(rows2['Lat']),      \
                             float(rows2['Long']),     \
                             float(rows2['Alt']),      \
                             float(rows1['Lat']),      \
                             float(rows1['Long']),     \
                             float(rows1['Alt']),      \
                             )                         \
                   <= distance ):
                        image_list.append(index2[-8:-4])
            final_list.append(image_list)
      df2= pd.DataFrame({'Images':final_list},index=video_dataframe.index)
      video_dataframe= pd.concat([video_dataframe,df2],axis=1)
      return(video_dataframe)


def haversine(lat1, lon1, alt1, lat2, lon2, alt2):
#Haversine helper function with a slight modification
       R = 6371000  # radius of Earth in meters
       phi_1 = radians(lat1)
       phi_2 = radians(lat2)
       delta_phi = radians(lat1 - lat2)
       delta_lambda = radians(lon1 - lon2)
       a = sin(delta_phi / 2.0) ** 2 + \
       cos(phi_1) * cos(phi_2) * \
       sin(delta_lambda / 2.0) ** 2
       c = 2 * atan2(sqrt(a), sqrt(1 - a))
       print(sqrt(pow((R * c),2)+ pow((alt1-alt2),2)))
       return(sqrt(pow((R * c),2)+ pow((alt1-alt2),2)))

def Create_KML(video_dataframe,kml_directory):
       video_dataframe.to_csv('Dronepath.csv')
       create_kml.createKML('Dronepath.csv',kml_directory)

