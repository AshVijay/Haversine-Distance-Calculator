import  pandas as pd
import numpy as np
import data_normalizer
import create_kml
import data_loader
import data_handler
import os

#Set Directories
Input_directory = "/home/ashwin/Downloads/Skylark Drones/software_dev"
Output_directory = "/home/ashwin/Downloads/Skylark Drones/software_dev/Output"
image_directory="/home/ashwin/Downloads/Skylark Drones/software_dev/images"
video_directory="/home/ashwin/Downloads/Skylark Drones/software_dev/videos"


#Set distance of interest in metres
distance = 100


def main():
    df1 = data_loader.Read_Images(image_directory)
    df2 = data_loader.Read_SRT(video_directory)

    if not os.path.exists(Output_directory):
        os.mkdir(Output_directory)
    os.chdir(Output_directory)

    print("Finding all images within ", distance , "meters from drone location")
    #Save Image outputs in excel format
    image_writer = pd.ExcelWriter('output.xlsx')
    data_handler.calc_Distance(df2, df1, distance).to_excel(image_writer,'Sheet1')
    image_writer.save()

    print("Finding all images within ", distance, "meters from Points of interest")
    #Save Point of Interest specific Outputs in Excel Format
    POI_writer = pd.ExcelWriter('POI_output.xlsx')
    data_handler.calc_POI(df1,Input_directory+"/"+'assets.csv',distance).to_excel(POI_writer,'Sheet1')
    POI_writer.save()

    #Create KML for drone path
    data_handler.Create_KML(df2, Output_directory)


if __name__ == '__main__':
      main()




