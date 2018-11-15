import exifread
import pandas as pd
import numpy as np
import os
import data_normalizer
import pysrt


def Read_Images(dir_path):
#Function to read EXIF data of images and store the values as a pandas data frame

  columns = ['Lat','Long','Alt']

  image_df=pd.DataFrame(columns=columns)
  #Create a pandas data frame to capture all the image data

  for _,_,filepaths in os.walk(dir_path):
    for filepath in sorted(filepaths):
        allowed_extensions = ['JPG','jpeg']
        try:
            if(filepath[-3:] in allowed_extensions):
               file=open(dir_path+"/"+filepath,'rb')
               tags = exifread.process_file(file)
            else:
                print("This particular file", filepath ,"does not have the correct extension")
                #To allow only image files to be read and other files to be ignored

        except:
            print("File open error")

        for tag in tags.keys():

          try:
            if tag == "GPS GPSAltitude":
                Alt = tags[tag]
            if tag == "GPS GPSAltitudeRef":
                AltRef = tags[tag]
            if tag == "GPS GPSLatitude":
                Lat = tags[tag]
            if tag == "GPS GPSLatitudeRef":
                LatRef = tags[tag]
            if tag == "GPS GPSLongitude":
                Long = tags[tag]
            if tag == "GPS GPSLongitudeRef":
                LongRef = tags[tag]

          except():
                print("Unable to load EXIF data")
        #print(Lat,Long,Alt)
        data= data_normalizer.match_patterns([str(Alt),str(AltRef),str(Lat),str(LatRef),str(Long),str(LongRef)])
        data= data_normalizer.convert(data)

        if(filepath[-3:] in allowed_extensions):
           temp_df=pd.DataFrame([[data[2],data[4],data[0]]],columns=columns,index=[filepath])
           image_df= pd.concat([image_df,temp_df],axis=0)
           #print(image_df)
  return(image_df)



def Read_SRT(dir_path):
#Function to read every SRT file from a folder of SRT files and capture the coordinates of the
#drone for every 100 milliseconds
    columns = ['Lat', 'Long','Alt']
    video_df = pd.DataFrame(columns=columns)

    # Create a pandas data frame to capture the coordinate values for every 100 milliseconds
    srt_list = []
    srt_names = []
    for _,_,file_paths in os.walk(dir_path): #The loop has complexity O(N^2) because theres provisioning for multiple SRT files as requested in the requirements
       for file_path in file_paths :
          allowed_extensions= ['SRT']
          if(file_path[-3:] == 'SRT'):
                      srt_list.append(pysrt.open(dir_path+"/"+file_path))
                      srt_names.append(file_path[-12:9])

          else:
                    print("No SRT found")

    names = -1
    for srt in srt_list: #The loop has complexity O(N^2) because theres provisioning for multiple SRT files as requested in the requirements
          count=0; names = names + 1
          time_interval = []
          for item in srt.text.split('\n'):
                   count += 100
                   time_interval.append(count)
                   lat  = item.split(',')[1]
                   long = item.split(',')[0]
                   alt  = item.split(',')[2]
                   temp_df = pd.DataFrame([[lat,long,alt]], columns=columns)
                   video_df = pd.concat([video_df, temp_df], axis=0)
          video_df.index= np.array(time_interval)
          print("\n\n\n Created Data Frame for the following SRT file - "+ srt_names[names]+"\n\n")
    return(video_df)


def Read_POI(file_path):
# Function to read the csv of Points of interests and convert it into a data frame
         POI_df= pd.read_csv(file_path)
         POI_df= POI_df.rename(columns= {'asset_name':'name','longitude':'Long', 'latitude':'Lat', 'image_names': 'Images'})
         POI_df['Alt']= np.array(0)
         POI_df = POI_df[['name','Lat','Long','Alt','Images']]
         return POI_df

