import csv
import simplekml
import os

def createKML(filepath,output_path):

     inputfile = csv.reader(open(filepath,'r'))
     kml=simplekml.Kml()
     if not os.path.exists(output_path):
         os.mkdir(output_path)
     os.chdir(output_path)
     for row in inputfile:
        kml.newpoint(name=row[0], coords=[(row[2],row[1])])
        kml.save('DronePath.kml')